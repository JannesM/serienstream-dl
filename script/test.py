import requests
import re


# ================= STAGE 1 =================
# with requests.Session() as session:

#   res = session.get("https://s.to/redirect/9015662")

#   with open("out.html", "wb") as f:
#     f.write(res.text.encode())

# ================= STAGE 2 =================
# with open("out.html", "rb") as f:
  
#   # read document
#   html = f.read().decode()

#   # remove whitespaces and line breaks
#   html = html.replace(" ", "").replace("\r\n", "").replace("\r", "").replace("\n", "").replace("\t", "")

#   # search string for data link
#   pattern = r"(?<=varsources={'hls':').*(?=','video_height)"
#   query = re.search(pattern, html)
#   print(query.group())

# ================= STAGE 3 =================
# master_link = "https://delivery-node-64by4o3ydkva40vc.voe-network.net/engine/hls2-c/01/00005/7u7k19x4ctfp_,n,.urlset/master.m3u8?t=YC9yCeEt1RCgQCHJKVA3juONOxeuztJjME6ACd_fHsk&s=1702813164&e=14400&f=7947392&node=delivery-node-2sswyguyhsj4lxd9.voe-network.net&i=31.150&sp=2500&asn=9145"

# with requests.Session() as session:

#   res = session.get(master_link)

#   with open("master.m3u8", "wb") as f:
#     f.write(res.text.encode())

# ================= STAGE 4 =================
# m3u8 readers
  
