1. Crie um repositório de imagens no IBM Cloud Container Registry:
ibmcloud cr namespace-add tnm-assistant-webhook

2. Faça login no IBM Cloud Container Registry:
ibmcloud cr login

3. Defina a região da IBM Cloud:
ibmcloud cr region-set global

4. Construa e envie sua imagem Docker:
docker build -t us.icr.io/tnm-assistant-webhook/assistant-webhook:latest .
docker push us.icr.io/tnm-assistant-webhook/assistant-webhook:latest

5. Crie uma aplicação no IBM Cloud Code Engine:
ibmcloud ce application create --name assistant-webhook \
  --image us.icr.io/tnm-assistant-webhook/assistant-webhook:latest \
  --cpu 0.5 --memory 512Mi --port 8080 \
  --env-from-secret ./ibmcloud.env

