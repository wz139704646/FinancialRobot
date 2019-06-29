from app.utils.DBHelper import MyHelper


class studentDao:
    def queryAll(self):
        myHelper = MyHelper()
        return myHelper.executeQuery("select * from student")


