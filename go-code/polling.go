package main

import (
	"context"
	"fmt"
	"log"
	"strconv"
	"time"

	"go.etcd.io/etcd/clientv3"
	"go.etcd.io/etcd/clientv3/concurrency"
)

func main() {

	cli, err := clientv3.New(clientv3.Config{
		Endpoints:   []string{"etcd.openshift-logging:2379"},
		DialTimeout: 5 * time.Second,
	})
	if err != nil {
		log.Fatal(err)
		return
	}
	defer cli.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Minute)
	defer cancel()

	session, err := concurrency.NewSession(cli)
	if err != nil {
		log.Fatal(err)
	}
	defer session.Close()

	mutex := concurrency.NewMutex(session, "etcd-lock")

	if err := mutex.Lock(context.TODO()); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Lock Aquired")

	getResp, err := cli.Get(ctx, "counter")
	if err != nil {
		log.Fatal(err)
	}

	val := string(getResp.Kvs[0].Value)
	numVal, err := strconv.Atoi(val)
	if err != nil {
		log.Fatal(err)
		return
	}
	value := strconv.Itoa(numVal - 1)

	putResp, err := cli.Put(ctx, "counter", value)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Put Respons:", putResp)

	if err := mutex.Unlock(context.TODO()); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Lock Released")
	fmt.Println("Waiting for all pods to complete...")

	for {
		getResp, err := cli.Get(ctx, "counter")
		if err != nil {
			log.Fatal(err)
		}
		val := string(getResp.Kvs[0].Value)
		numVal, err := strconv.Atoi(val)
		if numVal == 0 {
			break
		}
	}

	return
}
