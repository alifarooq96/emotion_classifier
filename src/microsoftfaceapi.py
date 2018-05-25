import http.client, urllib, base64
import json

headers = {
    # Request headers
    'Content-Type': 'application/json',
    
    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '611a0b762f9a441aa9fd113a659c239f',
}

params = urllib.parse.urlencode({
                          # Request parameters
                          'returnFaceId': 'true',
                          'returnFaceLandmarks': 'false',
                          'returnFaceAttributes': 'age,gender,blur,facialHair,smile,emotion',
                          })

def get_facial_features(url):
 
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('southeastasia.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, "{\"url\":\"" +url +"\"}", headers)

    response = conn.getresponse()

    data = response.read()
    
    conn.close()
    
    return data

def is_same_person(id1, id2):

    conn = http.client.HTTPSConnection('southeastasia.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/verify?%s" % params, "{\"faceId1\":\"" +id1 +"\", \"faceId2\":\"" +id2 +"\"}", headers)

    response = conn.getresponse()
    data = response.read()
    
    conn.close()
    data = json.loads(data)


    return data['isIdentical']
