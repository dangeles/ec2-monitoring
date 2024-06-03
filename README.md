# ec2-monitoring
Useful scripts to ensure you can monitor your ec2-instances

INSTRUCTIONS:
* ensure the base python has psutils installed
* place `monitoring.py` in the appropriate place (i like it in my base directory)
* add the `service` file to etc/systemd/system/monitor_usage.service

run in the terminal:
```
sudo systemctl daemon-reload
sudo systemctl restart monitor_usage.service
sudo systemctl status monitor_usage.service
```

profit

