import requests

url = "http://10.75.58.20:8080/api/running/sr-policy-service/"

payload = "<policy xmlns=\"http://example.com/sr_te\" xmlns:y=\"http://tail-f.com/ns/rest\"  xmlns:sr_te=\"http://example.com/sr_te\">\n  <policy_name>Alex15</policy_name>\n  <src_pe_name>R3</src_pe_name>\n  <pe_des_ip_address>7.47.47.78</pe_des_ip_address>\n  <color>10</color>\n  <preference>200</preference>\n  <binding_mpls_sid>23121</binding_mpls_sid>\n  <y:operations>\n    <check-sync>/api/running/sr-policy-service/policy/Alex13/_operations/check-sync</check-sync>\n    <deep-check-sync>/api/running/sr-policy-service/policy/Alex13/_operations/deep-check-sync</deep-check-sync>\n    <re-deploy>/api/running/sr-policy-service/policy/Alex13/_operations/re-deploy</re-deploy>\n    <reactive-re-deploy>/api/running/sr-policy-service/policy/Alex13/_operations/reactive-re-deploy</reactive-re-deploy>\n    <touch>/api/running/sr-policy-service/policy/Alex13/_operations/touch</touch>\n    <get-modifications>/api/running/sr-policy-service/policy/Alex13/_operations/get-modifications</get-modifications>\n    <un-deploy>/api/running/sr-policy-service/policy/Alex13/_operations/un-deploy</un-deploy>\n  </y:operations>\n</policy>"
headers = {
    'Content-Type': "application/vnd.yang.data+xml",
    'Authorization': "Basic YWRtaW46YWRtaW4=",
    'Cache-Control': "no-cache",
    'Postman-Token': "84b32051-9b30-448f-93c4-f702ea9c2639"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)