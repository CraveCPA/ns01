# Setup Kind Cluster with nginx ingress

```bash
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

Now since we are going to run this setup on local we would need to expose our application. For that we would need to simulate load balancer. There is a fantastic document avaialble with kind for install a <a href=https://kind.sigs.k8s.io/docs/user/loadbalancer/>Cloud Provider Kind</a> 

But before that we need to install golang on the system, if its not already present.  You can find the available go versions <a href=https://go.dev/dl/>here</a>

```golang installation
wget https://go.dev/dl/go1.23.8.linux-arm64.tar.gz

rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.8.linux-arm64.tar.gz

go version
```

```Installing cloud-provider-kind
go install sigs.k8s.io/cloud-provider-kind@latest

cp -pr go /usr/local/

```

The above command will add cloud-provider-kind binary in the /usr/local/go/bin directory. Exceute and run it in background. 
For ease of use I have create and run it as a service in the linux system so that i don't need to start it again on every restart.

* Create a file and place it in /etc/systemd/system directory, i have named it as cloud-provider-kind.service

``` cloud-provider-kind.service
[Unit]
Description=cloud-provider-kind

[service]
ExecStart=/usr/local/go/cloud-provider-kind

[Install]
WantedBy=multi-user.target
```

Then we reload the system daemon to read this unit file.
```
systemctl daemon-reload
```

Now we can run the service using systemctl and enable it to auto start on reboot.

```
systemctl start cloud-provider-kind
system enable cloud-provider-kind
```

Now that we have installed the cloud-provider-kind loadbalancer, lets setup ingress controller.

```
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
```

You can check the external IP address 
```
root@lab:~# kubectl get svc -n ingress-nginx
NAME                                 TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             LoadBalancer   10.96.159.55   172.18.0.3    80:30381/TCP,443:30488/TCP   48m
ingress-nginx-controller-admission   ClusterIP      10.96.80.184   <none>        443/TCP                      48m
root@lab:~#
```

All the applications will now be accessible on EXTERNAL IP, 172.18.0.3 in this case.



