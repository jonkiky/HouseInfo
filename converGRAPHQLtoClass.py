# -*- coding: utf-8 -*-

# read schema
def  readSchema(path):
     return [line.rstrip('\n') for line in open(path)]


# parser
def parser (list_string):
    list_of_clazz = []
    #read string
    # define a class
    clazz =[]
    # line of code to generate mock data
    clazz_data = []

    for line in list_string :
        if (line == ""):
            continue
        if("type" in line and "{" in line):  # check if that is start of class
            clazz = []
            #add name space
            clazz.append("package gov.nih.nci.icdc.mock.model;")
            clazz.append("public class  "+line[5:len(line)].upper())
            clazz_data = []
            # add construction function into it
            clazz_data.append("public" +line.replace("type","").replace("{","").upper()+"(){")
        elif("}" in line ):  # end of a class define
            # mock data
            for d in clazz_data:
                clazz.append(d)
            clazz.append("}") # for close construction function
            clazz.append("}") # for close class
            list_of_clazz.append(clazz)
        else:

            # find variable and type
            # example :
            #   case 1: created_datetime: String
            #   case 2: evaluations: [evaluation] @relation(name:"at_evaluation")
            index = line.find(':')
            variable = line[:index]
            type=line[index:len(line)]
            # check case 2
            if("[" in type):
                type=type[type.find("[")+1:type.find("]")].upper()

            clazz.append("public "+type.replace(":","")+" " +variable + " ;")

            if "id" in variable:
                clazz_data.append("this."+variable.strip()+"="+"\"123\";")
            elif "state" in variable:
                clazz_data.append("this."+variable.strip()+"="+"\" state \";")
            elif "datetime" in variable:
                clazz_data.append("this."+variable.strip()+"="+"\" 06/01/2019 \";")
            else:
                clazz_data.append("this." + variable.strip() + "=" + "\" "+variable.strip()+"_mock_data \";")

    return list_of_clazz


def writeTOJavaObject(list_of_class):
    for clazz in list_of_class:
        f = open("./tmp/"+clazz[1].replace("public","").replace("class","").replace("{","").strip()+".java", "w+")
        for line in clazz:
            f.write(line+"\n")
        f.close()


if __name__ == '__main__':
    print  writeTOJavaObject(parser(readSchema("/Users/cheny39/Desktop/icdc.graphqls")))