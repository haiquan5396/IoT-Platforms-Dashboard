#Start HomeAssitant


#Start OpenHab
```
export LINK=/home/ngocluanbka/Learning/IoT-Platforms-Dashboard/OH
```

```
    docker run --name='openhab_IPD' -p 8080:8080 -p 8443:8443 -v $LINK/addons:/openhab/addons -v $LINK/configurations:/openhab/configurations ngocluanbka/openhab
```