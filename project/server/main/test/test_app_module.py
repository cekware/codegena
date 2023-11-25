
def test_app_module():
    return True
#     foundation_module_import = ExportModuleImport(name="Foundation")
#     composable_module_import = ExportModuleImport(name="ComposableArchitecture")
#     network_module_import = ExportModuleImport(name="Network")

#     has_network_connection_state = ExportState(name="hasNetworkConnection", attribute="", access_control="", default_value="true", type="Bool", generic_of="",  is_array=False, isOptional=False, is_optional_generic=False)
#     token_state = ExportState(name="token", attribute="", access_control="", default_value=None, type="String", generic_of="",  is_array=False, isOptional=True, is_optional_generic=False)

#     setup_action = ExportAction(name="setupLaunch", module_name="TestModule", parameters=None)
#     update_network_connection_action = ExportAction(name="updateNetworkConnection", module_name="TestModule", parameters=[
#         ExportActionParameter(name="status", type="NWPath.Status", default_value=None, generic_of=None, is_array=False, isOptional=False, is_optional_generic=False)
#     ])

#     submodules = [
#         ExportSubmodule(name="destination", type="AppModuleOverlayDestination", presentation_type=1, related_module_name="AuthModule", isOptional=True, is_array=False, attribute="@PresentationState", default_value="", generic_of=""),
#         ExportSubmodule(name="transactionListState", type="TransactionListModule", presentation_type=0, related_module_name="TransactionListModule", isOptional=False, is_array=False, attribute="", default_value=".init()", generic_of="")
#     ]


#     module = ExportModule(
#         name="TestModule",
#         imports=[
#             foundation_module_import, 
#             composable_module_import
#             ],
#         states=[
#             has_network_connection_state,
#             token_state
#             ],
#         actions=[
#         setup_action,
#         update_network_connection_action
#         ],
#         submodules=submodules
#         )

#     assert module.name == "TestModule"

#     assert module.imports[0].name == "Foundation"
#     assert module.imports[1].name == "ComposableArchitecture"

#     assert module.states[0].as_swift_state_repr().strip() == "public var hasNetworkConnection: Bool = true"
#     assert module.states[1].as_swift_state_repr().strip() == "public var token: String?"

#     assert module.states[0].as_swift_init_parameter_repr().strip() == "hasNetworkConnection: Bool = true"
#     assert module.states[1].as_swift_init_parameter_repr().strip() == "token: String? = nil"

#     assert module.states[0].as_only_type().strip() == "Bool"
#     assert module.states[1].as_only_type().strip() == "String?"

#     assert module.actions[0].name.strip() == "setupLaunch"
#     assert module.actions[1].name.strip() == "updateNetworkConnection"

#     assert module.actions[0].swift_enum_repr().strip() == "case setupLaunch"
#     assert module.actions[1].swift_enum_repr().strip() == "case updateNetworkConnection(status: NWPath.Status)"


#     assert module.actions[0].swift_tca_func_definition_repr().strip() == "func setupLaunch(state: inout TestModule.State, action: TestModule.Action) -> Effect<TestModule.Action>"
#     assert module.actions[1].swift_tca_func_definition_repr().strip() == "func updateNetworkConnection(status: NWPath.Status, state: inout TestModule.State, action: TestModule.Action) -> Effect<TestModule.Action>"

#     assert module.actions[1].parameters[0].as_function_call_pair() == "status: status"
#     assert module.actions[1].parameters[0].as_type_repr() == "status: NWPath.Status"
#     assert module.actions[1].parameters[0].as_only_type() == "NWPath.Status"


#     assert module.submodules[0].name == "destination"
#     assert module.submodules[0].as_swift_submodule_repr() == "@PresentationState public var destination: AppModuleOverlayDestination.State?"
#     assert module.submodules[0].as_swift_init_parameter_repr() == "destination: AppModuleOverlayDestination.State? = nil"
#     assert module.submodules[0].as_only_type() == "AppModuleOverlayDestination.State?"
#     assert module.submodules[0].as_swift_tca_scopes_repr() == ".ifLet(\.$destination, action: /Action.destination){ AppModuleOverlayDestination() }"

#     assert module.submodules[1].name == "transactionListState"
#     assert module.submodules[1].as_swift_submodule_repr().strip() == "public var transactionListState: TransactionListModule.State = .init()"
#     assert module.submodules[1].as_swift_init_parameter_repr() == "transactionListState: TransactionListModule.State = .init()"
#     assert module.submodules[1].as_only_type() == "TransactionListModule.State"
#     assert module.submodules[1].as_swift_tca_scopes_repr() == "Scope(state: \.transactionListState, action: /Action.transactionListState){ TransactionListModule() }"

#     assert module.submodules[0].as_swift_tca_submodule_action_repr() == "case destination(PresentationAction<AppModuleOverlayDestination.Action>)"
#     assert module.submodules[1].as_swift_tca_submodule_action_repr() == "case transactionListState(TransactionListModule.Action)"



# if __name__ == "__main__":
#     test_app_module()