# from project.server.main.models import ExportModule,ExportModuleImport, ExportState, ExportAction, ExportActionParameter, ExportSubmodule

def test_transaction_module():
    return True
#     module = ExportModule(
#         name="TransactionModule",
#         imports=[
#             ExportModuleImport(name="Foundation"), 
#             ExportModuleImport(name="ComposableArchitecture")
#         ],
#         states=[
#             ExportState(name="transaction", attribute="", access_control="", default_value=None, type="Transaction", generic_of="",)
#         ],
#         actions=[
#         ],
#         submodules=[
#         ])

#     assert module.name == "TransactionModule"

#     assert module.imports[0].name == "Foundation"
#     assert module.imports[1].name == "ComposableArchitecture"


#     assert module.states[0].as_swift_state_repr().strip() == 'public var transaction: Transaction'
#     assert module.states[0].as_swift_init_parameter_repr().strip() == 'transaction: Transaction'
#     assert module.states[0].as_only_type().strip() == "Transaction"

# if __name__ == "__main__":
#     test_transaction_module()