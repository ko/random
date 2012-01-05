#include <linux/netdevice.h>    /* alloc_netdev */

/* pointers to net_device structs for sn0 and sn1 
 */
struct net_device *snull_devs[2];

/* allocating device structures 
 */
snull_devs[0] = alloc_netdev(sizeof(struct snull_priv), "sn%d",
        snull_init);
snull_devs[1] = alloc_netdev(sizeof(struct snull_priv), "sn%d",
        snull_init);
if (snull_devs[0] == NULL || snull_devs[1] == NULL)
    goto out;

/* net_device struct is initialized. complete registration by 
 * passing the structure to register_netdev()
 *
 * note:    as soon as you call register_netdev() your driver
 *          may be called to operate on the device. don't 
 *          register until everything initialized.
 */
for (i = 0; i < 2; i++)
    if ((result = register_netdev(snull_devs[i])))
        printk("snull: error %i registering device \"%s\"\n",
                result, snull_devs[i]->name);

/* initialize the net_device structure
 */
ether_setup(dev);

dev->open               = snull_open;
dev->stop               = snull_release;
dev->set_config         = snull_config;
dev->hard_start_xmit    = snull_tx; 
dev->do_ioctl           = snull_ioctl;
dev->get_stats          = snull_stats;
dev->rebuild_header     = snull_rebuild_header;
dev->hard_header        = snull_header;
dev->tx_timeout         = snull_tx_timeout;
dev->watchdog_timeo     = timeout;
/* keep the default falgs, just add NOARP */
dev->flags              |= IFF_NOARP;
dev->features           |= NETIF_F_NO_CSUM;
dev->hard_header_cache  = NULL; /* Disable caching */



struct snull_priv {
    struct net_device_stats stats;
    int status;
    struct snull_packet *ppool;
    struct snull_packet *rx_queue;  /* List of incoming packets */
    int rx_int_enabled;
    int tx_packetlen;
    u8 *tx_packetdata;
    struct sk_buff *skb;
    spinlock_t lock;
};


snull_init() 
{
    /* allocates and initializes the dev->priv */ 
    priv = netdev_priv(dev);
    memset(priv, 0, sizeof(struct snull_priv));
    spin_lock_init(&priv->lock);
    snull_rx_ints(dev, 1);  /* enble receive interrupts */
}

void snull_cleanup(void)
{
   int i;

  for (i = 0; i < 2; i++) {
      if (snull_devs[i]) {
          /* removes the interface from the system */
          unregister_netdev(snull_devs[i]);
          snull_teardown_pool(snull_devs[i]);
          /* returns the net_device struct to the kernel */
          free_netdev(snull_devs[i]);
      }
  }
  return;
}


int snull_open(struct net_device *dev)
{
    /* request_region(), request_irq(), ... (like fops->open) */

    /* assign the hardware address of the board: use "\0SNULx", where
     * x is 0 or 1. The first byte is '\0' to avoid being a multicast
     * address (the first byte of multicast addrs is odd).
     */
    memcpy(dev->dev_addr, "\0SNUL0", ETH_ALEN);
    if (dev == snull_devs[1])
        dev->dev_addr[ETH_ALEN-1]++; /* \0SNUL1 */
    netif_start-queue(dev); 
    return 0;
}

int snull_stop(struct net_device *dev)
{
    /* release_ports, irq and such -- like fops->close */

    netif_stop_queue(dev); /* can't transmit anymore! */
    return 0;
}

int snull_tx(struct sk_buff *skb, struct net_device *dev)
{
    int len;
    char *data, shortpkt[ETH_ZLEN];
    struct snull_priv *priv = netdev_priv(dev);

    data = skb->data;
    len = skb->len;
    if (len < ETH_ZLEN) {
        memset(shortpkt, 0, ETH_ZLEN);
        memcpy(shortpkt, skb->data, skb->len);
        len = ETH_ZLEN;
        data = shortpkt;
    }
    dev->trans_start = jiffies; /* save the timestamp */

    /* remember the skb, so we can free it at interrupt time */
    priv->skb = skb;

    /* actual delivery of data is device-specific. not shown here :( */
    snull_hw_tx(data, len, dev);

    /* failure is not an option. 
     * we've taken responsibility for this pkt 
     */
    return 0;
}

/* simulating transmitter lockups */
static int lockup = 0;
module_param(lockup, int, 0);   /* simul. every n packets tx'd */     

static int timeout = SNULL_TIMEOUT;
module_param(timeout, int, 0);  

/* snull transmission timeout handler 
 *
 * when transmission timeout happens, driver must mark the
 * error in the interface stats and arrange for device to be 
 * reset to a sane state so new pkts can be tx'd. 
 */
void snull_tx_timeout(struct net_device *dev)
{
    struct snull_priv *priv = netdev_priv(dev);
    PDEBUG("Transmit timeout at %ld, latency %ld\n", jiffies,
           jiffies - dev->trans_start);
    /* simulate a transmission interrupt to get things moving */
    priv->status = SNULL_TX_INTR;
    /* fills in missing interrupt */ 
    snull_interrupt(0, dev, NULL);
    priv->stats.tx_errors++;
    /* restart the tx queue */
    netif_wake_queue(dev);
    return;
}

void snull_rx(struct net_device *dev, struct snull_packet *pkt)
{
    struct sk_buff *skb;
    struct snull_priv *priv = netdev_priv(dev);

    /* the packet has been retrieved from the tx
     * medium. build an skb around it so upper layers
     * may have at it
     */
    skb = dev_alloc_skb(pkt->datalen + 2); /* kmalloc with atomicity */
    if (!skb) {
        if (printk_ratelimit())
            printk(KERN_NOTICE "snull rx: low on mem - packet dropped\n");
        priv->stats.rx_dropped++;
        goto out;
    }
    memcpy(skb_put(skb, pkt->datalen), pkt->data, pkt->datalen);

    /* write metadata, pass to receive level */
    skb->dev = dev;
    skb->protocol = eth_type_trans(skb, dev);
    skb->ip_summed = CHECKSUM_UNNECESSARY; /* no need to check it */
    priv->stats.rx_packets++;
    priv->stats.rx_bytes += pkt->datalen;
    netif_rx(skb); 
out:
    return;
}


static void snull_regular_interrupt(int irq, void *dev_id, struct pt_regs *regs)
{
    int statusword;
    struct snull_priv *priv;
    struct snull_packet *pkt = NULL;

    /* first task is to retrieve a ptr to the correct struct net_device
     *
     * as usual, check the 'device' ptr to be sure
     * it is really interrupting. 
     *
     * then assign "struct device *dev"
     */
    struct net_device *dev = (struct net_device *)dev_id;
    /* ... and check with hw if it's really ours */

    /* paranoid */
    if (!dev)
        return;

    /* lock the dev */
    priv = netdev_priv(dev);
    spin_lock(&priv->lock);

    /* retrieve statusword: real netdevices use IO instructions */
    statusword = priv->status;
    priv->status = 0;
    if (statusword & SNULL_RX_INTR) {
        /* send it to snull_rx for handling */
        pkt = priv->rx_queue;
        if (pkt) {
            priv->rx_queue = pkt->next;
            snull_rx(dev, pkt);
        }
    }
    if (statusword & SNULL_TX_INTR) {
        /* transmission is over: 
         *  update stats
         *  free the skb */
        priv->stats.tx_packets++;
        priv->stats.tx_bytes += priv->tx_packetlen;
        /* dev_kfree_skb
         *  - called only when you know code will not run in interrupt context
         *  (snull has no h/w interrupts)
         *
         * dev_kfree_skb_irq
         *  - optimized for freeing the buffer in an interrupt handler 
         *
         * dev_kfree_skb_any 
         *  - used for both in-and-out of int/nonint contexts
         */
        dev_kfree_skb(priv->skb);
    }
    /* if tx queue paused, restart with netif_wake_queue here */

    /* unlock the device and we are done */
    spin_unlock(&priv->lock);
    if (pkt) snull_release_buffer(pkt); /* do this outside the lock */
    return;
}

/*
 * budget:  max no. of pkts allowed to pass into the kernel
 *          max no. of pkts that the current CPU can rx from all interfaces
 */
static int snull_poll(struct net_device *dev, int *budget)
{
    /* dev->quota: per-interface value */ 
    int npackets = 0, quota = min(dev->quota, *budget);
    struct sk_buff *skb;
    struct snull_priv *priv = netdev_priv(dev);
    struct snull_packet *pkt;

    while (npackets < quota && priv->rx_queue) {
        pkt = snull_dequeue_buf(dev);
        skb = dev_alloc_skb(pkt->datalen + 2);
        if (!skb) {
            if (printk_ratelimit())
                printk(KERN_NOTICE "snull: packet dropped\n");
            priv->stats.rx_dropped++;
            snull_release_buffer(pkt);
            continue;
        }
        memcpy(skb_put(skb, pkt->datalen), pkt->data, pkt->datalen);
        skb->dev = dev;
        skb->protocol = eth_type_trans(skb, dev);
        skb->ip_summed = CHECKSUM_UNNECESSRY; /* don't check */
        /* use instead of netif_rx */
        netif_receive_skb(skb);

        /* stat maintenance */
        npackets++;
        priv->stats.rx_packets++;
        priv->stats.rx_bytes += pkt->datalen;
        snull_release_buffer(skb);
    }
    /* if all pkts processed, done; 
     * tell kernel + reenable ints */
    *budget -= npackets;
    dev->quota -= npackets; /* consistency */
    if (!priv->rx_queue) {
        netif_rx_complete(dev);
        snull_rx_ints(dev, 1);
        return 0;
    }
    /* couldn't process everything :( */
    return 1;
}

/* - takes info provided by kernel and formats it into a std Ethernet hdr 
 * - toggles bit in destination Ethernet address 
 */
int snull_header(struct sk_buff *skb, strut net_device *dev,
                unsigned short type, void *daddr, void *saddr,
                unsigned int len)
{
    struct ethhdr *eth = (struct ethhdr *)skb_push(skb,ETH_HLEN);

    eth->h_proto = htons(type);
    memcpy(eth->h_source, saddr ? saddr : dev->dev_addr, dev->addr_len);
    memcpy(eth->h_dest, daddr ? daddr : dev->dev_addr, dev->addr_len);
    eth->h_dest[ETH_ALEN-1] ^= 0x01;    /* dest is us xor 1 */ 
    return  (dev->hard_header_len);
}

