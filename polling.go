package main

// Copyright (c) <2019>, <Vladimir Masarik>

import (
	"context"
	"log"
	"os"

	"strconv"
	"time"

	"go.etcd.io/etcd/clientv3"
)

func getCounter(ctx context.Context, client *clientv3.Client) int {
	getResp, err := client.Get(ctx, "counter")
	if err != nil {
		log.Fatal(err)
	}

	nodeCount, err := strconv.Atoi(string(getResp.Kvs[0].Value))
	if err != nil {
		log.Fatal(err)
	}

	return nodeCount
}

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

	nodeCountBase, err := strconv.Atoi(os.Getenv("NODE_COUNT"))
	if err != nil {
		log.Fatal(err)
		return
	}

	keyValue := clientv3.NewKV(cli)
	_, err = keyValue.Txn(ctx).
		If(clientv3.Compare(clientv3.Version("counter"), "<", 1)).
		Then(clientv3.OpPut("counter", strconv.Itoa(nodeCountBase))).
		Commit()

	if err != nil {
		log.Fatal(err)
	}


	success := false
	for success == false {
		nodeCount := getCounter(ctx, cli)

		resp, err = keyValue.Txn(ctx).
			If(clientv3.Compare(clientv3.Value("counter"), "=", strconv.Itoa(nodeCount))).
			Then(clientv3.OpPut("counter", strconv.Itoa(nodeCount-1))).
			Commit()

		if err != nil {
			log.Fatal(err)
		}
		success = resp.Succeeded
	}
	

	log.Println("Waiting for all pods to complete...")

	if getCounter(ctx, cli) == 0 {
		return
	}

	responseChan := cli.Watch(ctx, "counter")
	for response := range responseChan {
		for _, event := range response.Events {
			if string(event.Kv.Value) == "0" {
				return
			}
		}
	}

	return
}
