import os

from flask_appbuilder.security.manager import AUTH_LDAP
from superset.security import SupersetSecurityManager


def obter_variavel(nome):
    valor = os.getenv(nome)

    if not valor:
        raise RuntimeError(
            f"A variável obrigatória {nome} não foi definida."
        )

    return valor


# Banco interno do Superset
SQLALCHEMY_DATABASE_URI = obter_variavel(
    "SUPERSET_DATABASE_URI"
)

# Chave utilizada para proteger sessões e cookies
SECRET_KEY = obter_variavel(
    "SUPERSET_SECRET_KEY"
)


# Tipo de autenticação
AUTH_TYPE = AUTH_LDAP


# Endereço interno do OpenLDAP na rede Docker
AUTH_LDAP_SERVER = "ldap://openldap:389"

# O laboratório local não utiliza TLS
AUTH_LDAP_USE_TLS = False


# Conta técnica utilizada para pesquisar usuários no LDAP
AUTH_LDAP_BIND_USER = obter_variavel(
    "LDAP_BIND_DN"
)

AUTH_LDAP_BIND_PASSWORD = obter_variavel(
    "LDAP_BIND_PASSWORD"
)


# Local onde o Superset pesquisará os usuários
AUTH_LDAP_SEARCH = "ou=usuarios,dc=empresa,dc=test"

# Campo utilizado como nome de login
AUTH_LDAP_UID_FIELD = "uid"


# Dados copiados do LDAP para o cadastro interno do Superset
AUTH_LDAP_FIRSTNAME_FIELD = "givenName"
AUTH_LDAP_LASTNAME_FIELD = "sn"
AUTH_LDAP_EMAIL_FIELD = "mail"


# Cria automaticamente o usuário no primeiro login
AUTH_USER_REGISTRATION = True

# Perfil padrão caso nenhum grupo seja reconhecido
AUTH_USER_REGISTRATION_ROLE = "Gamma"


# Campo LDAP que informa os grupos do usuário
AUTH_LDAP_GROUP_FIELD = "memberOf"


# Conversão dos grupos LDAP para perfis do Superset
AUTH_ROLES_MAPPING = {
    "cn=sistema_admins,ou=grupos,dc=empresa,dc=test": [
        "Admin"
    ],
    "cn=sistema_analistas,ou=grupos,dc=empresa,dc=test": [
        "Alpha"
    ],
    "cn=sistema_leitores,ou=grupos,dc=empresa,dc=test": [
        "Gamma"
    ],
}


# Atualiza o perfil em todos os logins
AUTH_ROLES_SYNC_AT_LOGIN = True


# Nome apresentado no sistema
APP_NAME = "POC de Provisionamento LDAP"


# Permite o funcionamento local usando HTTP
TALISMAN_ENABLED = False

class LdapSecurityManager(SupersetSecurityManager):
    def _ldap_calculate_user_roles(self, user_attributes):
        papeis_mapeados = set()

        if self.auth_roles_mapping:
            grupos_ldap = self.ldap_extract_list(
                user_attributes,
                self.auth_ldap_group_field,
            )

            papeis_mapeados.update(
                self.get_roles_from_keys(grupos_ldap)
            )

        # Se o usuário pertence a um grupo LDAP reconhecido,
        # recebe somente o papel correspondente.
        if papeis_mapeados:
            return list(papeis_mapeados)

        # Gamma será usado apenas como papel de segurança
        # caso nenhum grupo LDAP seja reconhecido.
        papel_padrao = self.find_role(
            self.auth_user_registration_role
        )

        if papel_padrao:
            return [papel_padrao]

        return []


CUSTOM_SECURITY_MANAGER = LdapSecurityManager
