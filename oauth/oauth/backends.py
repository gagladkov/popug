from oauth2_provider.scopes import SettingsScopes


class CustomScopesBackend(SettingsScopes):
    def get_default_scopes(self, application=None, request=None, *args, **kwargs):
        # смотрим на роль юзера и в зависимости от нее добавляем скопы в oauth
        default_scopes = ['introspection']
        if request and not request.user.is_anonymous:
            scopes = request.user.profile.role.scopes
            for scope in scopes.split():
                default_scopes.append(scope)
        return default_scopes
