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

