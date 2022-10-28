#

# 

`ifconf` structure

```c
/*
 * Structure used in SIOCGIFCONF request.
 * Used to retrieve interface configuration
 * for machine (useful for programs which
 * must know all networks accessible).
 */
struct ifconf {
    int ifc_len; /* size of buffer	*/
    union {
        char __user *ifcu_buf;
        struct ifreq __user *ifcu_req;
    } ifc_ifcu;
};
#define ifc_buf ifc_ifcu.ifcu_buf /* buffer address	*/
#define ifc_req ifc_ifcu.ifcu_req /* array of structures */
```



`ifreq` structure

```c
/*
 * Interface request structure used for socket
 * ioctl's.  All interface ioctl's must have parameter
 * definitions which begin with ifr_name.  The
 * remainder may be interface specific.
 */
struct ifreq {
#define IFHWADDRLEN 6
    union {
        char ifrn_name[IFNAMSIZ]; /* if name, e.g. "en0" */
    } ifr_ifrn;

    union {
        struct sockaddr ifru_addr;
        struct sockaddr ifru_dstaddr;
        struct sockaddr ifru_broadaddr;
        struct sockaddr ifru_netmask;
        struct sockaddr ifru_hwaddr;
        short ifru_flags;
        int ifru_ivalue;
        int ifru_mtu;
        struct ifmap ifru_map;
        char ifru_slave[IFNAMSIZ]; /* Just fits the size */
        char ifru_newname[IFNAMSIZ];
        void __user *ifru_data;
        struct if_settings ifru_settings;
    } ifr_ifru;
};
#define ifr_name ifr_ifrn.ifrn_name           /* interface name 	*/
#define ifr_hwaddr ifr_ifru.ifru_hwaddr       /* MAC address 		*/
#define ifr_addr ifr_ifru.ifru_addr           /* address		*/
#define ifr_dstaddr ifr_ifru.ifru_dstaddr     /* other end of p-p lnk	*/
#define ifr_broadaddr ifr_ifru.ifru_broadaddr /* broadcast address	*/
#define ifr_netmask ifr_ifru.ifru_netmask     /* interface net mask	*/
#define ifr_flags ifr_ifru.ifru_flags         /* flags		*/
#define ifr_metric ifr_ifru.ifru_ivalue       /* metric		*/
#define ifr_mtu ifr_ifru.ifru_mtu             /* mtu			*/
#define ifr_map ifr_ifru.ifru_map             /* device map		*/
#define ifr_slave ifr_ifru.ifru_slave         /* slave device		*/
#define ifr_data ifr_ifru.ifru_data           /* for use by interface	*/
#define ifr_ifindex ifr_ifru.ifru_ivalue      /* interface index	*/
#define ifr_bandwidth ifr_ifru.ifru_ivalue    /* link bandwidth	*/
#define ifr_qlen ifr_ifru.ifru_ivalue         /* Queue length 	*/
#define ifr_newname ifr_ifru.ifru_newname     /* New name		*/
#define ifr_settings ifr_ifru.ifru_settings   /* Device/proto settings*/
```

