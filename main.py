import json
from elasticsearch import Elasticsearch, BadRequestError
from dataclass.module import Module
# from dataclass import module

FOUNDRY_API_HEADERS: dict[str] = {
    "Content-Type": "application/json",
    "Authorization": "APIKey:foundryvtt_hkmg5t4zxc092e31mkfbg3",
}
FOUNDRY_API_BODY: dict[str] = {
    "type": "module",
    "version": "12.330",
    "license": {
        "host": "dontfight.club",
        "license": "2QBCHOEDLK5MDNX1RVCKNOMZ",
        "version": "11.293",
        "time": "2024-07-29T08:49:56.642Z",
        "signature": "Z2Og72EJvYuQscKsn7pwclRKGYPBJWvaEzaO0AC/WHlfKQ69Gt6WcuYNta1RN7k9W5diEVq0Ia/w0ztai9PsFxK4ms9xHLXH1UCzis0/1EDx11wilhdMvW8+j5Y920pofAi+IrS0vxm/pKbrR1LJXeu2S3ZQpgiGuZII61niWf/JbRT9uc3WLfN+xficl5aoKPSZeDvDcDS0IDG/U9idu5z/VKUQyaGALm3Vt2ujIaO1Uy9FDz/t+pvehWL4cQ3PJD/5/jg3vNLPLK70c6JqC01Mw+L7/M+XOTwudUE/tp+gqqWb0k/GQPDYDlSbzKVEPFztlrNQvfOFqN2WahZ2yTYjs//y6VRQg9wm3UDx9jI3WJne4LOSdnvd3mKV3WJpTNbnPlfnnsq494vp9qJl9S9qgCItPdAJEGm9rix/Zer6u8mOhv0j0W3yFs1GHIUCp5/eXXSuujIxGTFExALo/knPBD0bFzqA/1tEy85lMgyiPIzZR4gJ3aCW2RFQLfg9rPS7cPzdhVf7y6a6brWiyRqreR6chVFiBqKq4c5iInxRXEuiaFiO3l6cY5PPNcVyrMcsB0/0ZHjYQMG2KyKztLBSachtJDCPvjMoqtgULs3Fmfh0tiwQ+sECmSziKaFjnEHoB/4Sp6FwWSRxL2GaefQISW6rs7tpcd8vB62B428=",
    },
}
ELASTIC_API_KEY: str = "QkVwSkFKRUIyM1pfQVBpbjl6ZlA6bkdCempvbHhTQktIeTVodVhCT0RDdw=="
ELASTIC_SUPERUSER_PASS: str = "rAyby7M7vJK750KUCzIZ"
INDEX_NAME: str = "foundry_index"
MAPPING_NAME: str = "foundry_map"
FOUNDRY_MAPPING: str = open("mapping.json", "r").read()

client = Elasticsearch(
    "https://172.20.1.82:9200", api_key=ELASTIC_API_KEY, ca_certs="http-ca.crt"
)
try:
    client.indices.create(index=INDEX_NAME)
except BadRequestError as e:
    if e.message == "resource_already_exists_exception":
        print("Index already exists. Skipping....")
    else:
        print(e)
client.indices.put_mapping(index=INDEX_NAME, body=FOUNDRY_MAPPING)


def main():
    modules = []
    with open("data.json", "r") as datafile:
        datajson: dict = json.load(datafile)

    for module in datajson["packages"]:
        module: dict
        modules.append(
            Module(
                module["id"],
                module["name"],
                module["title"],
                module["description"],
                module["url"],
                bool(module["is_exclusive"]),
                bool(module["is_protected"]),
                module["author_username"],
                module["tags"],
                module["systems"],
                module["compatible_generation"],
                module["minimum"],
                module["verified"],
                module["maximum"],
                module["requires"],
                module["version"],
            )
        )

    for module in datajson["packages"]:
        # print(type(module))
        client.index(index=INDEX_NAME, id=module["id"], document=module)


if __name__ == "__main__":
    main()
