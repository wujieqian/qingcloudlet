Change Request 1
>&---------bad request------

bad request when sending http request. Here is the log of def _send_request(self, properties) in
i_qingcloud.py, line 61.

count 1
signature_method HmacSHA256
zone 'pek3a'
instance_type small_b
signature_version 1
signature VUy8Ek9RFyY51jSUQafd2tcjJJyMe3XgZIJAgepExVM%3D
instance_name test
image_id centos64x86a
vnets.1 vnet-0
version 1
access_key_id 'YFHFNVOBCPSMOAVFKQQU'
action RunInstances
url = count=1&signature_method=HmacSHA256&zone=%27pek3a%27&instance_type=small_b&signature_version=1&signature=VUy8Ek9RFyY51jSUQafd2tcjJJyMe3XgZIJAgepExVM%253D&instance_name=test&image_id=centos64x86a&vnets.1=vnet-0&version=1&access_key_id=%27YFHFNVOBCPSMOAVFKQQU%27&action=RunInstances
200

<html>
<head><title>400 Bad Request</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.1.19</center>
</body>
</html>
>&-------------