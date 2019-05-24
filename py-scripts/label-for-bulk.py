#!/usr/bin/env python3
import json
import random

INDEX_FIRST=0
INDEX_LAST=31



def main():
    with open("logs1400k.json", "rt", encoding="UTF-8") as f:
        for line in f:
            
            tup = line.strip()
            
            meta = "{{\"index\": {{\"_index\": \"nasa-{:03d}\", \"_type\": \"docs\"}}}}".format(random.randint(INDEX_FIRST, INDEX_LAST))

            res = "{}\n{}\n".format(meta,tup)
            print(res, end="")


if __name__ == "__main__":
    main()
