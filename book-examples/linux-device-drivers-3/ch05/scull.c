/*
 * Notice:
 *
 * We have a separate semaphore for every virtual scull device, rather than
 * a single global one. There's no reason to block one instance when
 * unnecessary.
 */
struct scull_dev {
    struct scull_qset *data;    /* pointer to first quantum set */
    int quantum;                /* current quantum size */
    int qset;                   /* current array size */
    unsigned long size;         /* amount of data stored here */
    unsigned int access_key;    /* used by sculluid and scullpriv */
    struct semaphore sem;       /* mutex semaphore */
    struct cdev cdev;           /* char dev struct */
}

/* 
 * Semaphores must be initialized before use. Perform this at initialization.
 */
for (i = 0; i < scull_nr_devs; i++) {
    scull_devices[i].quantum = scull_quantum;
    scull_devices[i].qset = scull_qset;
    /* 
     * Notice:
     *
     * 1. init_MUTEX cannot be found, replacing with sema_init(...,1)
     * init_MUTEX(&scull_devices[i].sem);
     *
     * 2. The semaphore must be initialized before making the scull devices
     * available to the rest of the system. Call scull_setup_cdev() after
     * the sema_init()
     */ 
    sema_init(&scull_devices[i].sem, 1);
    scull_setup_cdev(&scull_devices[i], i);
}

void scull_write() 
{
    /* We must have the scull semaphore before we make changes
     * to the scull_dev structure
     */
    if (down_interruptible(&dev->sem))
        /* The usual thing to do in this case is to return
         * -ERESTARTSYS. This tells the upper layers of
         * the kernel that they need to restart the call
         * from the beginning or return the error to the user
         *
         * If you return -ERESTARTSYS, you must first undo
         * any user-visible changes that may have been made,
         * so the correct set of operations occur when 
         * the call is retried.
         *
         * If you cannot undo the changes that have been
         * made, return -EINTR instead.
         */
        return -ERESTARTSYS;

out:
    /* Frees the semaphore and returns whatever status is called for.
     */
    up(&dev->sem);
    return retval; 
}
