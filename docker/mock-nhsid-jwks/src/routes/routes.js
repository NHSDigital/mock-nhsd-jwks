const identityServiceJWKS =  {
    method: 'GET',
    path: '/identity-service/jwks',
    handler: (request, h) => {    
        const path = 'IdTokenNHSIDIdentityServiceTestsJWKS.json'
        return h.file(path)
    }
  };

const healthCheck = {
  method: 'GET',
    path: '/_status',
    handler: (request, h) => {    
        const path = 'status.json'
        return h.file(path)
    }
}

module.exports = [identityServiceJWKS, healthCheck]
