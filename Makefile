# Project / Org
GCP_PROJECT ?= globalbridge-app
GKE_ZONE ?= europe-west4-b

# Service / App
GKE_CLUSTER_NAME ?= prod-cluster
RELEASE_NAME ?= converter
K8S_NS ?= prod-${RELEASE_NAME}
EXTERNAL_ADDRESS ?= ${RELEASE_NAME}.prod.globalbridge.app

# Docker Config
DOCKER_REPO ?= gcr.io/${GCP_PROJECT}
VERSION ?= $(shell cat VERSION)
DOCKER_TAG = ${DOCKER_REPO}/${RELEASE_NAME}:${VERSION}


ifeq (${SILENT},1)
	VERBOSE_TEST :=
else
	VERBOSE_TEST := -v
endif


release: build push

libdds/.git:
	git submodule update --init

build: 
	docker build -t ${DOCKER_TAG} .

push:
	docker push ${DOCKER_TAG}

deploy: set_gcp_context ensure_ns
	helm upgrade --install ${RELEASE_NAME} ./chart \
		--set image="${DOCKER_TAG}" \
		--set externalHostname="${EXTERNAL_ADDRESS}" \
		--namespace ${K8S_NS} \
#		--history-max=10

uninstall: set_gcp_context
	helm del ${RELEASE_NAME} --namespace ${K8S_NS}

set_gcp_context:
	gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone ${GKE_ZONE} --project ${GCP_PROJECT}

ensure_ns:
	kubectl create ns ${K8S_NS} || :

run_local_tests:
	python3 -m unittest discover ${VERBOSE_TEST}
