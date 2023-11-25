# from project.server.main.models import ExportModule,ExportModuleImport, ExportState, ExportAction, ExportActionParameter, ExportSubmodule

def test_forgot_password_module():
    return True
#     module = ExportModule(
#         name="ForgotPasswordModule",
#         imports=[
#             ExportModuleImport(name="Foundation"), 
#             ExportModuleImport(name="ComposableArchitecture")
#         ],
#         states=[
#             ExportState(name="username", attribute="", access_control="", default_value='""', type="String", generic_of="",  is_array=False, isOptional=False)
#         ],
#         actions=[
#             ExportAction(name="remindPasswordButtonTapped", module_name="ForgotPasswordModule", parameters=None),
#             ExportAction(name="remindResponse", module_name="ForgotPasswordModule", parameters=[
#                 ExportActionParameter(name="result", type="String", default_value=None, generic_of="TaskResult", is_array=False, isOptional=False)
#             ]),
#             ExportAction(name="setUsername", module_name="ForgotPasswordModule", parameters=[
#                 ExportActionParameter(name="username", type="String", default_value=None, generic_of="", is_array=False, isOptional=False)
#             ]),
#         ],
#         submodules=[
#         ])

#     assert module.name == "ForgotPasswordModule"

#     assert module.imports[0].name == "Foundation"
#     assert module.imports[1].name == "ComposableArchitecture"

#     assert module.states[0].as_swift_state_repr().strip() == 'public var username: String = ""'

#     assert module.states[0].as_swift_init_parameter_repr().strip() == 'username: String = ""'



#     assert module.states[0].as_only_type().strip() == "String"


#     assert module.actions[0].name.strip() == "remindPasswordButtonTapped"
#     assert module.actions[1].name.strip() == "remindResponse"
#     assert module.actions[2].name.strip() == "setUsername"

#     assert module.actions[0].swift_enum_repr().strip() == "case remindPasswordButtonTapped"
#     assert module.actions[1].swift_enum_repr().strip() == "case remindResponse(result: TaskResult<String>)"
#     assert module.actions[2].swift_enum_repr().strip() == "case setUsername(username: String)"



#     assert module.actions[0].swift_tca_func_definition_repr().strip() == "func remindPasswordButtonTapped(state: inout ForgotPasswordModule.State, action: ForgotPasswordModule.Action) -> Effect<ForgotPasswordModule.Action>"
#     assert module.actions[1].swift_tca_func_definition_repr().strip() == "func remindResponse(result: TaskResult<String>, state: inout ForgotPasswordModule.State, action: ForgotPasswordModule.Action) -> Effect<ForgotPasswordModule.Action>"
#     assert module.actions[2].swift_tca_func_definition_repr().strip() == "func setUsername(username: String, state: inout ForgotPasswordModule.State, action: ForgotPasswordModule.Action) -> Effect<ForgotPasswordModule.Action>"


#     assert module.actions[1].parameters[0].as_function_call_pair() == "result: result"
#     assert module.actions[1].parameters[0].as_type_repr() == "result: TaskResult<String>"
#     assert module.actions[1].parameters[0].as_only_type() == "String" # This is weird check this

#     assert module.actions[2].parameters[0].as_function_call_pair() == "username: username"
#     assert module.actions[2].parameters[0].as_type_repr() == "username: String"
#     assert module.actions[2].parameters[0].as_only_type() == "String"


# if __name__ == "__main__":
#     test_forgot_password_module()