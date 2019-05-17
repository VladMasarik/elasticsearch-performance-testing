package main

import (
	"context"
	"log"
	"os"
	"time"

	"go.etcd.io/etcd/clientv3"
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

	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Minute)
	defer cancel()

	putResp, err := cli.Put(ctx, "counter", os.Getenv("NODE_COUNT"))
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Put Respons:", putResp)
	return
}
