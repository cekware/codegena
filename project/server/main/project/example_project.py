# from project.server.main.objects import User, Project, Module, State, Action, Parameter, Submodule, SubmoduleType, ModuleImport

from project.server.main.objects.module import Module
from project.server.main.objects.moduleimport import ModuleImport
from project.server.main.objects.state import State
from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter
from project.server.main.objects.submodule import Submodule

from project.server.main.objects.enums import SubmoduleType


from project.server import db


def example_app(project):
    

    transaction_module = Module(project=project, name="TransactionModule", description="Transaction module description")

    transaction_composableArchitecture = ModuleImport(name="ComposableArchitecture", module=transaction_module)
    transaction_foundation = ModuleImport(name="Foundation", module=transaction_module)
    
    transaction_transaction_state = State(name="transaction", type="Transaction", is_mutable=True, module=transaction_module)

    db.session.add_all([transaction_module])
    db.session.add_all([transaction_composableArchitecture, transaction_foundation])
    db.session.add_all([transaction_transaction_state])

    # Commit everything
    db.session.commit()



    # FORGOT MODULE
    forgotPasswordModule = Module(project=project, name="ForgotPasswordModule", description="RegisterModule description")

    forgot_composableArchitecture = ModuleImport(name="ComposableArchitecture", module=forgotPasswordModule)
    forgot_foundation = ModuleImport(name="Foundation", module=forgotPasswordModule)

    forgot_username_state = State(name="username", type="String", default_value='""', module=forgotPasswordModule)

    forgot_setusername_action = Action(name="setUsername", module=forgotPasswordModule)
    forgot_setusername_action_parameter = Parameter(type="String", name="username", action=forgot_setusername_action)

    forgot_remind_action = Action(name="remindPasswordButtonTapped", module=forgotPasswordModule)

    forgot_remind_response_action = Action(name="remindResponse", module=forgotPasswordModule)
    forgot_remind_response_action_parameter = Parameter(type="String", name="result", generic_of="TaskResult", action=forgot_remind_response_action)


    db.session.add_all([forgotPasswordModule])
    db.session.add_all([forgot_composableArchitecture, forgot_foundation])
    db.session.add_all([forgot_username_state])

    db.session.add_all([
        forgot_setusername_action,
        forgot_remind_action, 
        forgot_remind_response_action
        ])
    db.session.add_all([
        forgot_setusername_action_parameter,
        forgot_remind_response_action_parameter
        ])

    # REGISTER MODULE
    registerModule = Module(project=project, name="RegisterModule", description="RegisterModule description")

    register_composableArchitecture = ModuleImport(name="ComposableArchitecture", module=registerModule)
    register_foundation = ModuleImport(name="Foundation", module=registerModule)

    register_username_state = State(name="username", type="String", default_value='""', module=registerModule)
    register_password_State = State(name="password", type="String", default_value='""', module=registerModule)
    register_password_confirm_state = State(name="passwordConfirm", type="String", default_value='""', module=registerModule)

    register_setusername_action = Action(name="setUsername", module=registerModule)
    register_setusername_action_parameter = Parameter(type="String", name="username", default_value='""', action=register_setusername_action)

    register_set_password_action = Action(name="setPassword", module=registerModule)
    register_set_password_action_parameter = Parameter(type="String", name="password", default_value='""', action=register_set_password_action)
    
    regiseter_set_password_confirm_action = Action(name="setPasswordConfirm", module=registerModule)
    regiseter_set_password_confirm_action_paramter = Parameter(type="String", name="passwordConfirm", default_value='""', action=regiseter_set_password_confirm_action)

    register_register_action = Action(name="registerButtonTapped", module=registerModule)

    register_register_response_action = Action(name="registerResponse", module=registerModule)
    register_register_response_action_parameter = Parameter(type="String", name="result", generic_of="TaskResult", action=register_register_response_action)

    db.session.add_all([registerModule])
    db.session.add_all([register_composableArchitecture, register_foundation])
    db.session.add_all([
        register_username_state,
        register_password_State, 
        register_password_confirm_state
        ])

    db.session.add_all([
        register_setusername_action,
        register_set_password_action, 
        regiseter_set_password_confirm_action,
        register_register_action, 
        register_register_response_action
          ])
    db.session.add_all([
        register_setusername_action_parameter,
        register_set_password_action_parameter, 
        regiseter_set_password_confirm_action_paramter, 
        register_register_response_action_parameter
        ])

    # TRANSACTION LIST MODULE
    transaction_list_module = Module(project=project, name="TransactionListModule", description="AppModule description")

    tl_path_submodule = Submodule(module=transaction_list_module, reference=transaction_module, name="transaction", type="TransactionDestination", presentation_type=SubmoduleType.Stack)


    tl_composableArchitecture = ModuleImport(name="ComposableArchitecture", module=transaction_list_module)
    tl_foundation = ModuleImport(name="Foundation", module=transaction_list_module)

    tl_all_transactions_state = State(name="allTransactions", type="Transaction", is_mutable=True, is_array=True, default_value="[]", module=transaction_list_module)
    tl_filtered_transactions_state = State(name="filteredAndSortedTransactions", type="Transaction", is_mutable=True, is_array=True, default_value="[]", module=transaction_list_module)    
    tl_transaction_total_state = State(name="transactionsTotal", type="Transaction.Detail.Value", is_mutable=True, is_optional=True, module=transaction_list_module)
    tl_selected_category_state = State(name="selectedCategory", type="Transaction.Category", is_mutable=True, default_value=".all", module=transaction_list_module)   
    tl_selected_direction_state = State(name="selectedSortDirection", type="TransactionSortDirection", is_mutable=True, default_value=".bookingDateDesc", module=transaction_list_module)   
    # state6 = State(name="path", type="TransactionListDestination.State", generic_of="StackState", is_mutable=True, default_value=".init()", module=transactionListModule)   
    # state7 = State(attribute="@PresentationState", name="alert", generic_of="AlertState", type="Action", is_mutable=True, isOptional_generic=True, module=transactionListModule)   
    tl_loading_state = State(name="isLoading", type="Bool", is_mutable=True, default_value="true", module=transaction_list_module)   


    tl_load_action = Action(name="loadTransactions", module=transaction_list_module)
    tl_wait_load_action = Action(name="waitAndLoad", module=transaction_list_module)
    
    tl_load_response_action = Action(name="loadTransactionsResponse", module=transaction_list_module)
    tl_load_response_action_parameter = Parameter(type="Transaction", is_array=True, generic_of="TaskResult", name="result", action=tl_load_response_action)

    tl_update_total_action = Action(name="updateTransactionTotal", module=transaction_list_module)


    tl_total_updated_action = Action(name="transactionsTotalUpdated", module=transaction_list_module)
    tl_total_updated_action_parameter = Parameter(type="Transaction.Detail.Value", generic_of="TaskResult", name="value", action=tl_total_updated_action)

    tl_set_selected_category_action = Action(name="setSelectedCategory", module=transaction_list_module)
    tl_set_selected_category_action_parameter = Parameter(type="Transaction.Category", name="category", action=tl_set_selected_category_action)

    tl_set_selected_direction_action = Action(name="setSelectedSortDirection", module=transaction_list_module)
    tl_set_selected_direction_action_parameter = Parameter(type="TransactionSortDirection", name="direction", action=tl_set_selected_direction_action)

    # action8 = Action(name="path", module=transactionListModule)
    # parameter5 = Parameter(type="TransactionListDestination.State, TransactionListDestination.Action", name="path", generic_of="StackAction", action=action8)

    tl_transactions_action = Action(name="transactions", module=transaction_list_module)
    tl_transactions_action_parameter1 = Parameter(type="TransactionModule.State.ID", name="id", action=tl_transactions_action)
    tl_transactions_action_parameter2 = Parameter(type="TransactionModule.Action", name="action", action=tl_transactions_action)

    # action10 = Action(name="alert", module=transactionListModule)
    # parameter8 = Parameter(type="TransactionListModule.Action", name="alertAction", generic_of="PresentationAction", action=action10)

    tl_retry_action = Action(name="retryAction", module=transaction_list_module)

    db.session.add_all([transaction_list_module])
    db.session.add_all([tl_path_submodule])
    db.session.add_all([tl_composableArchitecture, tl_foundation])
    db.session.add_all([
        tl_all_transactions_state, 
        tl_filtered_transactions_state, 
        tl_transaction_total_state, 
        tl_selected_category_state, 
        tl_selected_direction_state, 
        tl_loading_state
        ])
    db.session.add_all([
        tl_load_action, 
        tl_wait_load_action,
        tl_load_response_action,
        tl_update_total_action,
        tl_total_updated_action,
        tl_set_selected_category_action, 
        tl_set_selected_direction_action, 
        tl_transactions_action,
        tl_retry_action
        ])
    db.session.add_all([
        tl_load_response_action_parameter, 
        tl_total_updated_action_parameter, 
        tl_set_selected_category_action_parameter, 
        tl_set_selected_direction_action_parameter, 
        tl_transactions_action_parameter1, 
        tl_transactions_action_parameter2
        ])
    





    appModule = Module(project=project, name="AppModule", description="AppModule description")

    app_composableArchitecture = ModuleImport(name="ComposableArchitecture", module=appModule)
    app_foundation = ModuleImport(name="Foundation", module=appModule)
    app_network = ModuleImport(name="Network", module=appModule)
    
    # destinationSubModule = Submodule(module=appModule, name="destination", type="AppModuleOverlayDestination", presentation_type=SubmoduleType.Presentation, isOptional=True, is_array=False, attribute="@PresentationState")
    
    listSubModule = Submodule(module=appModule, reference=transaction_list_module, name="transactionListState", type="TransactionListModule", default_value=".init()")
    # state2 = State(name="", type=".State", default_value=".init()", is_mutable=True, module=appModule)    

    # state1 = State(attribute="@PresentationState", name="destination", type="AppModuleOverlayDestination.State", is_mutable=True, isOptional=True, module=appModule)
    hasNetworkConnectionState = State(name="hasNetworkConnection", type="Bool", is_mutable=True, default_value="true", module=appModule)
    tokenState = State(name="token", type="String", is_mutable=True, is_optional=True, module=appModule)   


    setup_action = Action(name="setupLaunch", module=appModule)
    update_connection_action = Action(name="updateNetworkConnection", module=appModule)
    update_connection_action_parameter = Parameter(type="NWPath.Status", name="status", action=update_connection_action)

    db.session.add_all([appModule])
    db.session.add_all([app_composableArchitecture, app_foundation, app_network])
    db.session.add_all([
        listSubModule
        ])
    db.session.add_all([
        hasNetworkConnectionState, 
        tokenState
        ])
    db.session.add_all([
        setup_action, 
        update_connection_action
        ])
    db.session.add_all([update_connection_action_parameter])

    auth_module = Module(project=project, name="AuthModule", description="AppModule description")
    
    auth_composableArchitecture = ModuleImport(name="ComposableArchitecture", module=auth_module)
    auth_foundation = ModuleImport(name="Foundation", module=auth_module)
    
    auth_username_state = State(name="username", type="String", default_value='""', module=auth_module)
    auth_password_state = State(name="password", type="String", default_value='""', module=auth_module)
    auth_destination_submodule = Submodule(module=auth_module, reference=registerModule, name="register", presentation_type=SubmoduleType.Presentation, is_optional=True)
    auth_destination_submodule1 = Submodule(module=auth_module, reference=forgotPasswordModule, name="forgotPassword", presentation_type=SubmoduleType.Presentation, is_optional=True)

    login_action = Action(name="loginButtonTapped", module=auth_module)

    login_response_action = Action(name="loginResponse", module=auth_module)
    login_response_action_parameter = Parameter(type="String", name="token", generic_of="TaskResult", action=login_response_action)


    auth_set_username_action = Action(name="setUsername", module=auth_module)
    auth_set_username_action_parameter = Parameter(type="String", name="username", default_value='""', action=auth_set_username_action)

    auth_set_password_action = Action(name="setPassword", module=auth_module)
    auth_set_password_action_parameter = Parameter(type="String", name="password", default_value='""', action=auth_set_password_action)

    auth_forgot_action = Action(name="forgotPasswordButtonTapped", module=auth_module)
    auth_register_action = Action(name="registerButtonTapped", module=auth_module)
    
    db.session.add_all([auth_module])
    db.session.add_all([auth_composableArchitecture, auth_foundation])
    db.session.add_all([auth_destination_submodule, auth_destination_submodule1])
    
    db.session.add_all([
        auth_username_state,
        auth_password_state
        ])

    db.session.add_all([
        login_action,
        login_response_action, 
        auth_set_username_action, 
        auth_set_password_action, 
        auth_forgot_action,
        auth_register_action
        ])
    db.session.add_all([
        login_response_action_parameter,
        auth_set_username_action_parameter,
        auth_set_password_action_parameter
        ])
