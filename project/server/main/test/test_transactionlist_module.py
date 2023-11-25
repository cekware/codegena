# from project.server.main.models import ExportModule,ExportModuleImport, ExportState, ExportAction, ExportActionParameter, ExportSubmodule

def test_transaction_list_module():
    return True
#     module = ExportModule(
#         name="TransactionListModule",
#         imports=[
#             ExportModuleImport(name="Foundation"), 
#             ExportModuleImport(name="ComposableArchitecture")
#             ],
#         states=[
#             ExportState(name="allTransactions", attribute="", access_control="", default_value='[]', type="Transaction", generic_of="",  is_array=True, isOptional=False, isOptional_generic=False),
#             ExportState(name="transactionsTotal", attribute="", access_control="", default_value=None, type="Transaction.Detail.Value", generic_of="",  is_array=False, isOptional=True, isOptional_generic=False),
#             ExportState(name="selectedCategory", attribute="", access_control="", default_value=".all", type="Transaction.Category", generic_of="",  is_array=False, isOptional=False, isOptional_generic=False),
#             ExportState(name="selectedSortDirection", attribute="", access_control="", default_value=".bookingDateDesc", type="TransactionSortDirection", generic_of="",  is_array=False, isOptional=False, isOptional_generic=False),
#             ExportState(name="isLoading", attribute="", access_control="", default_value="true", type="Bool", generic_of="", is_array=False, isOptional=False, isOptional_generic=False)
#             ],
#         actions=[
#             ExportAction(name="loadTransactions", module_name="TransactionListModule", parameters=None),
#             ExportAction(name="waitAndLoad", module_name="TransactionListModule", parameters=None),
#             ExportAction(name="loadTransactionsResponse", module_name="TransactionListModule", parameters=[
#                 ExportActionParameter(name="result", type="Transaction", default_value=None, generic_of="TaskResult", is_array=True, isOptional_generic=False)
#             ]),
#             ExportAction(name="updateTransactionTotal", module_name="TransactionListModule", parameters=None),
#             ExportAction(name="transactionsTotalUpdated", module_name="TransactionListModule", parameters=[
#                 ExportActionParameter(name="value", type="Transaction.Detail.Value", default_value=None, generic_of="TaskResult",  isOptional=True, isOptional_generic=False)
#             ]),
#             ExportAction(name="setSelectedCategory", module_name="TransactionListModule", parameters=[
#                 ExportActionParameter(name="category", type="Transaction.Category", default_value=None, generic_of=None,   isOptional_generic=False)
#             ]),
#             ExportAction(name="setSelectedSortDirection", module_name="TransactionListModule", parameters=[
#                 ExportActionParameter(name="direction", type="TransactionSortDirection", default_value=None, generic_of=None, isOptional_generic=False)
#             ]),
#             ExportAction(name="retryAction", module_name="TransactionListModule", parameters=None)
#             ],
#         submodules=[
#             ExportSubmodule(name="filteredAndSortedTransactions", type="TransactionModule", presentation_type=0, related_module_name="TransactionModule",  is_array=True, attribute="", default_value="[]", generic_of=""),
#         ])

#     assert module.name == "TransactionListModule"

#     assert module.imports[0].name == "Foundation"
#     assert module.imports[1].name == "ComposableArchitecture"

#     assert module.states[0].as_swift_state_repr().strip() == 'public var allTransactions: [Transaction] = []'

#     assert module.states[0].as_swift_init_parameter_repr().strip() == 'allTransactions: [Transaction] = []'
#     assert module.states[0].as_only_type().strip() == "[Transaction]"

#     assert module.states[1].as_swift_state_repr().strip() == 'public var transactionsTotal: Transaction.Detail.Value?'
#     assert module.states[1].as_swift_init_parameter_repr().strip() == 'transactionsTotal: Transaction.Detail.Value? = nil'
#     assert module.states[1].as_only_type().strip() == "Transaction.Detail.Value?"

#     assert module.states[2].as_swift_state_repr().strip() == 'public var selectedCategory: Transaction.Category = .all'
#     assert module.states[2].as_swift_init_parameter_repr().strip() == 'selectedCategory: Transaction.Category = .all'
#     assert module.states[2].as_only_type().strip() == "Transaction.Category"

#     assert module.states[3].as_swift_state_repr().strip() == 'public var selectedSortDirection: TransactionSortDirection = .bookingDateDesc'
#     assert module.states[3].as_swift_init_parameter_repr().strip() == 'selectedSortDirection: TransactionSortDirection = .bookingDateDesc'
#     assert module.states[3].as_only_type().strip() == "TransactionSortDirection"

#     assert module.states[4].as_swift_state_repr().strip() == 'public var isLoading: Bool = true'
#     assert module.states[4].as_swift_init_parameter_repr().strip() == 'isLoading: Bool = true'
#     assert module.states[4].as_only_type().strip() == "Bool"



#     assert module.actions[0].name.strip() == "loadTransactions"
#     assert module.actions[1].name.strip() == "waitAndLoad"
#     assert module.actions[2].name.strip() == "loadTransactionsResponse"
#     assert module.actions[3].name.strip() == "updateTransactionTotal"
#     assert module.actions[4].name.strip() == "transactionsTotalUpdated"
#     assert module.actions[5].name.strip() == "setSelectedCategory"
#     assert module.actions[6].name.strip() == "setSelectedSortDirection"
#     assert module.actions[7].name.strip() == "retryAction"

#     assert module.actions[0].swift_enum_repr().strip() == "case loadTransactions"
#     assert module.actions[1].swift_enum_repr().strip() == "case waitAndLoad"
#     assert module.actions[2].swift_enum_repr().strip() == "case loadTransactionsResponse(result: TaskResult<[Transaction]>)"
#     assert module.actions[3].swift_enum_repr().strip() == "case updateTransactionTotal"
#     assert module.actions[4].swift_enum_repr().strip() == "case transactionsTotalUpdated(value: TaskResult<Transaction.Detail.Value?>)"
#     assert module.actions[5].swift_enum_repr().strip() == "case setSelectedCategory(category: Transaction.Category)"
#     assert module.actions[6].swift_enum_repr().strip() == "case setSelectedSortDirection(direction: TransactionSortDirection)"
#     assert module.actions[7].swift_enum_repr().strip() == "case retryAction"



#     assert module.actions[0].swift_tca_func_definition_repr().strip() == "func loadTransactions(state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[1].swift_tca_func_definition_repr().strip() == "func waitAndLoad(state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[2].swift_tca_func_definition_repr().strip() == "func loadTransactionsResponse(result: TaskResult<[Transaction]>, state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[3].swift_tca_func_definition_repr().strip() == "func updateTransactionTotal(state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[4].swift_tca_func_definition_repr().strip() == "func transactionsTotalUpdated(value: TaskResult<Transaction.Detail.Value?>, state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[5].swift_tca_func_definition_repr().strip() == "func setSelectedCategory(category: Transaction.Category, state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[6].swift_tca_func_definition_repr().strip() == "func setSelectedSortDirection(direction: TransactionSortDirection, state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"
#     assert module.actions[7].swift_tca_func_definition_repr().strip() == "func retryAction(state: inout TransactionListModule.State, action: TransactionListModule.Action) -> Effect<TransactionListModule.Action>"


#     assert module.actions[2].parameters[0].as_function_call_pair() == "result: result"
#     assert module.actions[2].parameters[0].as_type_repr() == "result: TaskResult<[Transaction]>"
#     assert module.actions[2].parameters[0].as_only_type() == "[Transaction]" # This is weird check this

#     assert module.actions[4].parameters[0].as_function_call_pair() == "value: value"
#     assert module.actions[4].parameters[0].as_type_repr() == "value: TaskResult<Transaction.Detail.Value?>"
#     assert module.actions[4].parameters[0].as_only_type() == "Transaction.Detail.Value?"

#     assert module.actions[5].parameters[0].as_function_call_pair() == "category: category"
#     assert module.actions[5].parameters[0].as_type_repr() == "category: Transaction.Category"
#     assert module.actions[5].parameters[0].as_only_type() == "Transaction.Category"

#     assert module.actions[6].parameters[0].as_function_call_pair() == "direction: direction"
#     assert module.actions[6].parameters[0].as_type_repr() == "direction: TransactionSortDirection"
#     assert module.actions[6].parameters[0].as_only_type() == "TransactionSortDirection"

#     assert module.submodules[0].name == "filteredAndSortedTransactions"
#     assert module.submodules[0].as_swift_submodule_repr() == " public var filteredAndSortedTransactions: IdentifiedArrayOf<TransactionModule.State> = []"
#     assert module.submodules[0].as_swift_init_parameter_repr() == "filteredAndSortedTransactions: IdentifiedArrayOf<TransactionModule.State> = []"
#     assert module.submodules[0].as_only_type() == "IdentifiedArrayOf<TransactionModule.State>"
#     assert module.submodules[0].as_swift_tca_scopes_repr() == ".forEach(\.filteredAndSortedTransactions, action: /Action.filteredAndSortedTransactions){ TransactionModule() }"

#     assert module.submodules[0].as_swift_tca_submodule_action_repr() == "case filteredAndSortedTransactions(id: filteredAndSortedTransactions.State.ID, action: TransactionModule.Action)"


# if __name__ == "__main__":
#     test_transaction_list_module()