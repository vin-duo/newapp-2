from hello import db

print('db: {}'.format(db) )
db.drop_all()
print('db deletado')
db.create_all()
print('db criado')


