# Kubernetes Monitoring Pod

This project is designed to deploy a **monitoring pod in Kubernetes** that allows interaction with the cluster in order to perform basic health, resource, and storage checks.  
The monitoring logic runs inside the cluster and communicates directly with the Kubernetes API.

---

##  Requirements

- A running Kubernetes cluster (k8s, k3s, EKS, etc.)
- `kubectl` access to the cluster
- An **NFS server** accessible from the cluster

---

##  Installation and Configuration

### 1 Create the namespace

Create the namespace where the monitoring pod will be deployed:

```bash
kubectl create namespace kubernetes-monitoring

```
### 2 Copy monitoring scripts to NFS
Copy the contents of the monitory/ directory into the NFS path configured for the pod. <br/>
<strog>his directory will be mounted inside the pod and used to execute the monitoring scripts.</strong>

### 3 Configure email credentials
Edit the following file:

`modules/mail/sendmail.py`

Configure the following values:
* **Sender email**
* **Recipient email(s)**
* **SMTP password / credentials**

**Example:**
```python
sender = "monitor@gmail.com"
receiver = ["admin@mydomain.com"]
password = "********"
```

### 4 Deploy the monitoring pod
Apply the Kubernetes manifest located in the kubernetes/ directory:

```bash
kubectl apply -f kubernetes/monitoring-pod-deployment.yaml
```