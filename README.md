# Template for deploying k3s backed by Flux

Highly opinionated template for deploying a single [k3s](https://k3s.io) cluster with [Ansible](https://www.ansible.com) and [Terraform](https://www.terraform.io) backed by [Flux](https://toolkit.fluxcd.io/) and [SOPS](https://toolkit.fluxcd.io/guides/mozilla-sops/).

Based on prior work from:

+ [k8s-at-home/template-cluster-k3s](https://github.com/k8s-at-home/template-cluster-k3s)
+ [onedr0p/homelab](https://github.com/onedr0p/homelab)
+ [blackjid/k8s-gitops](https://github.com/blackjid/k8s-gitops)
+ [billimek/k8s-gitops](https://github.com/billimek/k8s-gitops)
