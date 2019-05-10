#!/usr/bin/env python3
import json
import random

INDEX_FIRST=0
INDEX_LAST=31



def main():
    i = 0
    with open("logs1400k.json", "rt", encoding="UTF-8") as f:
        for line in f:
            i += 1
            
            
            tup = line.strip()
            
            meta = "{{\"index\": {{\"_index\": \"nasa-{:03d}\", \"_type\": \"docs\"}}}}".format(random.randint(INDEX_FIRST, INDEX_LAST))
            #meta = "{{\"index\": {{\"_index\": \"nasa-{:03d}\", \"_type\": \"docs\"}}}}".format(0)


            # x = random.randint(1,3)
            # if x == 1:
            #     meta = "{{\"index\": {{\"_index\": \"nasaone\", \"_type\": \"docs\", \"_id\": \"{}\"}}}}".format(i)
            # elif x == 2:
            #     meta = "{{\"index\": {{\"_index\": \"nasatwo\", \"_type\": \"docs\", \"_id\": \"{}\"}}}}".format(i)
            # else:
            #     meta = "{{\"index\": {{\"_index\": \"nasatre\", \"_type\": \"docs\", \"_id\": \"{}\"}}}}".format(i)



            res = "{}\n{}\n".format(meta,tup)
            print(res, end="")


if __name__ == "__main__":
    main()
