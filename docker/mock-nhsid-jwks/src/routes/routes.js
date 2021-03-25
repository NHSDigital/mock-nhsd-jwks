const identityServiceJWKS =  {
    method: 'GET',
    path: '/identity-service/jwks',
    handler: (request, h) => {
        const path = 'IdTokenNHSIDIdentityServiceTestsJWKS.json'
        return h.file(path)
    }
  };

const nhsLoginJWKS =  {
  method: 'GET',
  path: '/identity-service/nhs-login-jwks',
  handler: (request, h) => {
    const path = 'IdTokenNHSLoginServiceTestsJWKS.json'
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

const userRoleService = {
  method: ['GET', 'POST', 'PUT'],
  path: '/user-role-service',
  handler: (request, h) => {
    const path = 'userRoleService.json'
    return h.file(path)
  }
}

module.exports = [identityServiceJWKS, nhsLoginJWKS, healthCheck, userRoleService]
