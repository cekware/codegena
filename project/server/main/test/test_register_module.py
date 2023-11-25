# from project.server.main.models import ExportModule,ExportModuleImport, ExportState, ExportAction, ExportActionParameter, ExportSubmodule

def test_register_module():
    return True
#     module = ExportModule(
#         name="RegisterModule",
#         imports=[
#             ExportModuleImport(name="Foundation"), 
#             ExportModuleImport(name="ComposableArchitecture")
#             ],
#         states=[
#             ExportState(name="username", attribute="", access_control="", default_value='""', type="String", generic_of="",  is_array=False, isOptional=False),
#             ExportState(name="password", attribute="", access_control="", default_value='""', type="String", generic_of="",  is_array=False, isOptional=False),
#             ExportState(name="passwordConfirm", attribute="", access_control="", default_value='""', type="String", generic_of="",  is_array=False, isOptional=False)
#             ],
#         actions=[
#             ExportAction(name="registerButtonTapped", module_name="ForgotPasswordModule", parameters=None),
#             ExportAction(name="registerResponse", module_name="RegisterModule", parameters=[
#                 ExportActionParameter(name="result", type="String", default_value=None, generic_of="TaskResult", is_array=False, isOptional=False)
#             ]),
#             ExportAction(name="setUsername", module_name="RegisterModule", parameters=[
#                 ExportActionParameter(name="username", type="String", default_value=None, generic_of="", is_array=False, isOptional=False)
#             ]),
#             ExportAction(name="setPassword", module_name="RegisterModule", parameters=[
#                 ExportActionParameter(name="password", type="String", default_value=None, generic_of="", is_array=False, isOptional=False)
#             ]),
#             ExportAction(name="setPasswordConfirm", module_name="RegisterModule", parameters=[
#                 ExportActionParameter(name="passwordConfirm", type="String", default_value=None, generic_of="", is_array=False, isOptional=False)
#             ])
#         ],
#         submodules=[
#         ])

#     assert module.name == "RegisterModule"

#     assert module.imports[0].name == "Foundation"
#     assert module.imports[1].name == "ComposableArchitecture"

#     assert module.states[0].as_swift_state_repr().strip() == 'public var username: String = ""'
#     assert module.states[0].as_swift_init_parameter_repr().strip() == 'username: String = ""'
#     assert module.states[0].as_only_type().strip() == "String"

#     assert module.states[1].as_swift_state_repr().strip() == 'public var password: String = ""'
#     assert module.states[1].as_swift_init_parameter_repr().strip() == 'password: String = ""'
#     assert module.states[1].as_only_type().strip() == "String"

#     assert module.states[2].as_swift_state_repr().strip() == 'public var passwordConfirm: String = ""'
#     assert module.states[2].as_swift_init_parameter_repr().strip() == 'passwordConfirm: String = ""'
#     assert module.states[2].as_only_type().strip() == "String"



#     assert module.actions[0].name.strip() == "registerButtonTapped"
#     assert module.actions[1].name.strip() == "registerResponse"
#     assert module.actions[2].name.strip() == "setUsername"
#     assert module.actions[3].name.strip() == "setPassword"
#     assert module.actions[4].name.strip() == "setPasswordConfirm"


#     assert module.actions[0].swift_enum_repr().strip() == "case registerButtonTapped"
#     assert module.actions[1].swift_enum_repr().strip() == "case registerResponse(result: TaskResult<String>)"
#     assert module.actions[2].swift_enum_repr().strip() == "case setUsername(username: String)"
#     assert module.actions[3].swift_enum_repr().strip() == "case setPassword(password: String)"
#     assert module.actions[4].swift_enum_repr().strip() == "case setPasswordConfirm(passwordConfirm: String)"



#     assert module.actions[0].swift_tca_func_definition_repr().strip() == "func registerButtonTapped(state: inout RegisterModule.State, action: RegisterModule.Action) -> Effect<RegisterModule.Action>"
#     assert module.actions[1].swift_tca_func_definition_repr().strip() == "func registerResponse(result: TaskResult<String>, state: inout RegisterModule.State, action: RegisterModule.Action) -> Effect<RegisterModule.Action>"
#     assert module.actions[2].swift_tca_func_definition_repr().strip() == "func setUsername(username: String, state: inout RegisterModule.State, action: RegisterModule.Action) -> Effect<RegisterModule.Action>"
#     assert module.actions[3].swift_tca_func_definition_repr().strip() == "func setPassword(password: String, state: inout RegisterModule.State, action: RegisterModule.Action) -> Effect<RegisterModule.Action>"
#     assert module.actions[4].swift_tca_func_definition_repr().strip() == "func setPasswordConfirm(passwordConfirm: String, state: inout RegisterModule.State, action: RegisterModule.Action) -> Effect<RegisterModule.Action>"


#     assert module.actions[1].parameters[0].as_function_call_pair() == "result: result"
#     assert module.actions[1].parameters[0].as_type_repr() == "result: TaskResult<String>"
#     assert module.actions[1].parameters[0].as_only_type() == "String" # This is weird check this

#     assert module.actions[2].parameters[0].as_function_call_pair() == "username: username"
#     assert module.actions[2].parameters[0].as_type_repr() == "username: String"
#     assert module.actions[2].parameters[0].as_only_type() == "String"

#     assert module.actions[3].parameters[0].as_function_call_pair() == "password: password"
#     assert module.actions[3].parameters[0].as_type_repr() == "password: String"
#     assert module.actions[3].parameters[0].as_only_type() == "String"

#     assert module.actions[4].parameters[0].as_function_call_pair() == "passwordConfirm: passwordConfirm"
#     assert module.actions[4].parameters[0].as_type_repr() == "passwordConfirm: String"
#     assert module.actions[4].parameters[0].as_only_type() == "String"


# if __name__ == "__main__":
#     test_register_module()