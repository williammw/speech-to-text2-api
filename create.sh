# Variables
RESOURCE_GROUP_NAME="flask-aks-openai-rg"
LOCATION="CentralUS"
ACR_NAME="flaskaksacr"
APP_SERVICE_PLAN_NAME="flask-aks-app-service-plan"
APP_NAME="flask-aks-openai-app"
IMAGE_NAME="flask-aks-openai-image"
SUBSCRIPTION_ID="21463751-2d01-40fe-979a-6dfdf7b68dc6"

# 1. Log in to your Azure account
az login

# 2. Create a resource group
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# 3. Create an Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP_NAME --name $ACR_NAME --sku Basic --admin-enabled true

# 4. Create an Azure App Service plan
az appservice plan create --name $APP_SERVICE_PLAN_NAME --resource-group $RESOURCE_GROUP_NAME --sku B1 --is-linux

# 5. Create an Azure App Service web app with a container
az webapp create --resource-group $RESOURCE_GROUP_NAME --plan $APP_SERVICE_PLAN_NAME --name $APP_NAME --deployment-container-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:latest

# 6. Configure the web app to use the container registry
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
az webapp config container set --name $APP_NAME --resource-group $RESOURCE_GROUP_NAME --docker-custom-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:latest --docker-registry-server-url https://$ACR_NAME.azurecr.io --docker-registry-server-user $ACR_NAME --docker-registry-server-password $ACR_PASSWORD

# 7. Get the AZURE_CREDENTIALS secret value
az ad sp create-for-rbac --name "$APP_NAME" --sdk-auth --role contributor --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME

# 8. Get the REGISTRY_USERNAME and REGISTRY_PASSWORD secret values
az acr credential show --name $ACR_NAME

# 9. Get the AZURE_APP_SERVICE_PUBLISH_PROFILE secret value
az webapp deployment list-publishing-profiles --name $APP_NAME --resource-group $RESOURCE_GROUP_NAME --query "[0].publishProfile" -o tsv

# 10. 
az webapp deployment list-publishing-profiles --name $APP_NAME --resource-group $RESOURCE_GROUP_NAME
