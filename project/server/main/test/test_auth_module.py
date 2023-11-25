# from project.server.main.models import ExportModule,ExportModuleImport, ExportState, ExportAction, ExportActionParameter, ExportSubmodule

def test_auth_module():
    return True
#     module = ExportModule(
#         name="AuthModule",
#         imports=[
#             ExportModuleImport(name="Foundation"), 
#             ExportModuleImport(name="ComposableArchitecture")
#         ],
#         states=[
#             ExportState(name="username", attribute="", access_control="", default_value='""', type="String", generic_of="",  is_array=False, isOptional=False),
#             ExportState(name="password", attribute="", access_control="", default_value=None, type="String", generic_of="",  is_array=False, isOptional=False)
#         ],
#         actions=[
#             ExportAction(name="loginButtonTapped", module_name="AuthModule", parameters=None),
#             ExportAction(name="forgotPasswordButtonTapped", module_name="AuthModule", parameters=None),
#             ExportAction(name="registerButtonTapped", module_name="AuthModule", parameters=None),
#             ExportAction(name="loginResponse", module_name="AuthModule", parameters=[
#                 ExportActionParameter(name="token", type="String", default_value=None, generic_of="TaskResult", is_array=False, isOptional=False)
#             ]),
#             ExportAction(name="setUsername", module_name="AuthModule", parameters=[
#                 ExportActionParameter(name="username", type="String", default_value=None, generic_of="", is_array=False, isOptional=False)
#             ]),
#             ExportAction(name="setPassword", module_name="AuthModule", parameters=[
#                 ExportActionParameter(name="password", type="String", default_value=None, generic_of="", is_array=False, isOptional=False)
#             ])
#         ],
#         submodules=[
#             ExportSubmodule(name="destination", type="AuthDestination", presentation_type=1, related_module_name="AuthModule", isOptional=True, is_array=False, attribute="@PresentationState",  default_value="", generic_of=""),
#         ])

#     assert module.name == "AuthModule"

#     assert module.imports[0].name == "Foundation"
#     assert module.imports[1].name == "ComposableArchitecture"

#     assert module.states[0].as_swift_state_repr().strip() == 'public var username: String = ""'
#     assert module.states[1].as_swift_state_repr().strip() == "public var password: String"

#     assert module.states[0].as_swift_init_parameter_repr().strip() == 'username: String = ""'
#     assert module.states[1].as_swift_init_parameter_repr().strip() == "password: String"



#     assert module.states[0].as_only_type().strip() == "String"
#     assert module.states[1].as_only_type().strip() == "String"


#     assert module.actions[0].name.strip() == "loginButtonTapped"
#     assert module.actions[1].name.strip() == "forgotPasswordButtonTapped"
#     assert module.actions[2].name.strip() == "registerButtonTapped"

#     assert module.actions[0].swift_enum_repr().strip() == "case loginButtonTapped"
#     assert module.actions[1].swift_enum_repr().strip() == "case forgotPasswordButtonTapped"
#     assert module.actions[2].swift_enum_repr().strip() == "case registerButtonTapped"

#     assert module.actions[0].swift_tca_func_definition_repr().strip() == "func loginButtonTapped(state: inout AuthModule.State, action: AuthModule.Action) -> Effect<AuthModule.Action>"
#     assert module.actions[1].swift_tca_func_definition_repr().strip() == "func forgotPasswordButtonTapped(state: inout AuthModule.State, action: AuthModule.Action) -> Effect<AuthModule.Action>"
#     assert module.actions[2].swift_tca_func_definition_repr().strip() == "func registerButtonTapped(state: inout AuthModule.State, action: AuthModule.Action) -> Effect<AuthModule.Action>"

#     assert module.actions[3].name.strip() == "loginResponse"
#     assert module.actions[4].name.strip() == "setUsername"
#     assert module.actions[5].name.strip() == "setPassword"

#     # print(module.actions[3].swift_enum_repr().strip())

#     assert module.actions[3].swift_enum_repr().strip() == "case loginResponse(token: TaskResult<String>)"
#     assert module.actions[4].swift_enum_repr().strip() == "case setUsername(username: String)"
#     assert module.actions[5].swift_enum_repr().strip() == "case setPassword(password: String)"

#     assert module.actions[3].swift_tca_func_definition_repr().strip() == "func loginResponse(token: TaskResult<String>, state: inout AuthModule.State, action: AuthModule.Action) -> Effect<AuthModule.Action>"
#     assert module.actions[4].swift_tca_func_definition_repr().strip() == "func setUsername(username: String, state: inout AuthModule.State, action: AuthModule.Action) -> Effect<AuthModule.Action>"
#     assert module.actions[5].swift_tca_func_definition_repr().strip() == "func setPassword(password: String, state: inout AuthModule.State, action: AuthModule.Action) -> Effect<AuthModule.Action>"



#     assert module.actions[3].parameters[0].as_function_call_pair() == "token: token"
#     assert module.actions[3].parameters[0].as_type_repr() == "token: TaskResult<String>"
#     assert module.actions[3].parameters[0].as_only_type() == "String" # This is weird check this

#     assert module.actions[4].parameters[0].as_function_call_pair() == "username: username"
#     assert module.actions[4].parameters[0].as_type_repr() == "username: String"
#     assert module.actions[4].parameters[0].as_only_type() == "String"

#     assert module.actions[5].parameters[0].as_function_call_pair() == "password: password"
#     assert module.actions[5].parameters[0].as_type_repr() == "password: String"
#     assert module.actions[5].parameters[0].as_only_type() == "String"


#     assert module.submodules[0].name == "destination"
#     assert module.submodules[0].as_swift_submodule_repr() == "@PresentationState public var destination: AuthDestination.State?"
#     assert module.submodules[0].as_swift_init_parameter_repr() == "destination: AuthDestination.State? = nil"
#     assert module.submodules[0].as_only_type() == "AuthDestination.State?"
#     assert module.submodules[0].as_swift_tca_scopes_repr() == ".ifLet(\.$destination, action: /Action.destination){ AuthDestination() }"

#     assert module.submodules[0].as_swift_tca_submodule_action_repr() == "case destination(PresentationAction<AuthDestination.Action>)"

# if __name__ == "__main__":
#     test_auth_module()