import time, os


def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


# from project.server.main.objects import User, Project, Module, State, Action, Parameter
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration

from jinja2 import Template, FileSystemLoader, Environment

def create_export_task(project_id):
    # project = Project.query.filter_by(id=project_id).first()
    # user = project.owner
    # code = user.code
    # repo_name = project.name.strip()
    
    # auth = Auth.Token(code)
    # g = Github(auth=auth)
    # repo = g.get_repo(repo_name)
    
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # data_file = os.path.join(basedir, '../../client/static/templates/tca')
    
    # env = Environment(
    #     loader = FileSystemLoader(data_file)
    # )
    
    # package_swift_name = "Package.swift"
    # package_template = env.get_template('package.txt')
    # package_swift_content = package_template.render(project=project)
    # try:
    #     contents = repo.get_contents(package_swift_name)
    #     repo.update_file(contents.path, "Update package.swift", package_swift_content, contents.sha)
    # except:
    #     repo.create_file(package_swift_name, "Create package.swift", package_swift_content)
    
    # test_swift_name = "Tests/{}Tests.swift".format(project.short_name)
    # test_template = env.get_template('test.txt')
    # test_swift_content = test_template.render(project=project)
    # try:
    #     contents = repo.get_contents(test_swift_name)
    #     repo.update_file(contents.path, "Update Tests", test_swift_content, contents.sha)
    # except:
    #     repo.create_file(test_swift_name, "Create Tests", test_swift_content)

    # extra_swift_name = "Sources/{}/Extra.swift".format(project.short_name)
    # extra_template = env.get_template('extra_file.txt')
    # extra_swift_content = extra_template.render()
    # try:
    #     contents = repo.get_contents(extra_swift_name)
    #     repo.update_file(contents.path, "Update Extra", extra_swift_content, contents.sha)
    # except:
    #     repo.create_file(extra_swift_name, "Create Extra", extra_swift_content)

    
    # for module in project.modules:
    #     export_module = ExportModule.fromModule(module)
    #     module_name = "Sources/{}/{}.swift".format(project.short_name, module.name)
    #     if module.extra_info == "navigation":
    #         template = env.get_template('navigation.txt')
    #     else:
    #         template = env.get_template('module.txt')

    #     result = template.render(module=export_module)
    #     try:
    #         contents = repo.get_contents(module_name)
    #         repo.update_file(contents.path, "Update {}".format(module.name), result, contents.sha)
    #     except:
    #         repo.create_file(module_name, "Create {}".format(module.name), result)


    return True   