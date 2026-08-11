# Kubernetes deployment

This directory provides a Kustomize deployment for the split setup in the
root `compose.yml`. It runs PostgreSQL, Redis, and separate web, worker,
consumer, and scheduler containers in the `paperless` namespace.

## Prerequisites

- A Kubernetes cluster with a default `StorageClass`.
- An RWX-capable storage provisioner for the Paperless shared volumes.
- The four application images built and available to the cluster:
  `paperless-web:2.20.1`, `paperless-worker:2.20.1`,
  `paperless-consumer:2.20.1`, and `paperless-scheduler:2.20.1`.

The base uses placeholder credentials matching `compose.yml`. Change
`k8s/base/secret-generator.yaml` in a private overlay, or replace the
generated Secret with an external secret manager before deploying anywhere
other than a disposable local cluster. Do not commit production credentials.

## Build and publish images

The role-specific images can be built from the repository root:

```bash
docker build --build-arg PAPERLESS_ROLE=web -t paperless-web:2.20.1 .
docker build --build-arg PAPERLESS_ROLE=worker -t paperless-worker:2.20.1 .
docker build --build-arg PAPERLESS_ROLE=consumer -t paperless-consumer:2.20.1 .
docker build --build-arg PAPERLESS_ROLE=scheduler -t paperless-scheduler:2.20.1 .
```

For a remote cluster, tag each image with a registry name and push it. Then
set the image names in an overlay, for example with Kustomize's `images`
field.

## Deploy

Render the manifests without applying them:

```bash
kubectl kustomize k8s/overlays/local
```

Apply them to the current cluster:

```bash
kubectl apply -k k8s/overlays/local
kubectl -n paperless get pods,pvc
```

Access the web service locally with port forwarding:

```bash
kubectl -n paperless port-forward service/paperless-web 8008:8000
```

Paperless is then available at <http://localhost:8008>.

## Storage notes

PostgreSQL and Redis use dedicated `ReadWriteOnce` claims. The Paperless
`data`, `media`, `consume`, `export`, and temporary processing directories
are shared by multiple Deployments and therefore use `ReadWriteMany` claims.
The cluster's storage provisioner must support RWX, or those claims must be
patched to match the provisioner and scheduling model.
