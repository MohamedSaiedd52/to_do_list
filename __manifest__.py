{
    'name':'todo_management',
    'author':'Mohamed Saied',
    'version':'1.0',
    'depends':['base','mail','snailmail'],
    'data':[
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/to_do.xml',
        'data/automatic_actions.xml',
        'reports/task_report.xml'
        
    ],
    'assets':{
        'web.assets_backend':['to_do_list/static/src/css/to_do.css']
    },
    'application':True,
    'installable':True,
}