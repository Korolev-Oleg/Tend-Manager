restore = {
    "default": [
        {
            'val': ''
        },{
            'val': ''
        },{
            'val': ''
        },{
            'val': ''
        },{
            'val': ''
        },{
            'val': ''
        }

    ]
}
print(restore, end='\n\n')

df = restore['default']

df[3]['val'] = 11111111111111111
print(restore)

# print(restore, end='\n\n')