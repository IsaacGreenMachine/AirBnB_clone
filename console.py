#!/usr/bin/python3
"""Module for the console"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import dict_greyson, storage


class HBNBCommand(cmd.Cmd):
    """class for the command console"""
    prompt = '(hbnb)'

    def emptyline(self):
        """behavior for an empty line"""
        pass

    def do_EOF(self, args):
        """
        Exits the console
        """
        return True

    def do_quit(self, args):
        """
        Exits the Console
        """
        return True

    def do_create(self, args):
        """
        Creates a new instance of a class
        and prints its id
        Usage: create <Class Name>
        Ex: create BaseModel
        """
#       error handling
        argList = args.split(" ")
        if len(argList[0]) == 0:
            print("** class name missing **")
        elif argList[0] not in dict_greyson.keys():
            print("** class doesn't exist **")
        else:
            objClass = dict_greyson[argList[0]]
#           creates a new base model
            b = objClass()
#           saves to json doc
            b.save()
#           prints ID
            print(b.id)

    def do_show(self, args):
        """
        Prints the string representation of
        an instance
        Usage: show <class name> <id>
        Ex: show BaseModel 1234-1234-1234
        """
        #  array of words from args#
        strArr = args.split(" ")
        #  error handling
        if len(args) == 0:
            print("** class name missing **")
        elif strArr[0] not in dict_greyson.keys():
            print("** class doesn't exist **")
        elif len(strArr) < 2:
            print("** instance id missing **")
        else:
            #  name = cls.ID#
            name = strArr[0] + "." + strArr[1]
            #  dict of all obj in class.ID: obj format
            d = storage.all()
            #  gets object from dict based on name
            item = d.get(name)
            #  error handling
            if item is None:
                print("** no instance found **")
            #  prints object
            else:
                print(item)

    def do_destroy(self, args):
        """
        Deletes an instance
        Usage: destroy <class name> <id>
        Ex: destroy BaseModel 1234-1234-1234
        """
        #  array of words from args
        strArr = args.split(" ")
        #  error handling
        if len(args) == 0:
            print("** class name missing **")
            return
        elif strArr[0] not in dict_greyson.keys():
            print("** class doesn't exist **")
            return
        elif len(strArr) < 2:
            print("** instance id missing **")
            return
#       name = class.ID
        name = strArr[0] + "." + strArr[1]
#       dict of all obj in class.ID: obj format
        d = storage.all()
#       gets object based on name
        item = d.get(name)
#       error handling
        if item is None:
            print("** no instance found **")
#       deletes object from dictionary
        else:
            del d[name]
            storage.save()

    def do_all(self, args):
        """
        Displays all istances of a given class
        or all instances if no class is specified
        Usage: all <class name>
        Ex: all
            lists all instances
        Ex: all BaseModel
            lists all instances of BaseModel
        """
        #  dict of all obj in class.ID: obj format
        d = storage.all()
        #  final list
        objList = []
        #  Printing all objects
        if len(args) == 0:
            #  o is name in class.ID format
            for o in d:
                #  gets object for each name
                item = d.get(o)
                #  adds str rep of each obj to list
                objList.append(str(item))
        #  Printing only specified objects
        else:
            #  array of words from args
            strArr = args.split(" ")
            #  checks if word is a recognized type
            if strArr[0] not in dict_greyson.keys():
                print("** class doesn't exist **")
                return
            else:
                #  o is name in class.ID format
                for o in d:
                    #  splits cls.ID into cls and ID
                    nameSplitArr = o.split(".")
                    #  checks if class is recognized
                    if nameSplitArr[0] == strArr[0]:
                        #  gets object for each name
                        item = d.get(o)
                        #  adds str rep of each obj to list
                        objList.append(str(item))
        #  prints list of str formatted objects
        print(objList)

    def do_update(self, args):
        """
        Updates an attribute of an instance
        Usage: update <class name> <id> <attribute> "<attribute value>"
        Ex: update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        #  dict of all obj in class.ID: obj format
        d = storage.all()
        #  if args is empty
        if len(args) == 0:
            print("** class name missing **")
            return
        #  array of words from args
        strArr = args.split(" ", 3)
        if strArr[0] not in dict_greyson.keys():
            print("** class doesn't exist **")
            return
        if len(strArr) > 1:
            obj = d.get(strArr[0] + "." + strArr[1])
            if obj is None:
                print("** no instance found **")
                return
        if len(strArr) < 4:
            if len(strArr) == 1:
                print("** instance id missing **")
            elif len(strArr) == 2:
                print("** attribute name missing **")
            else:
                print("** value missing **")
            return
        else:
            try:
                # gets object
                if strArr[3][0] != '"':
                    print("** value missing **")
                    return
                for i in range(1, len(strArr[3])):
                    if strArr[3][i] == '"':
                        break
                if strArr[3][i] != '"':
                    print("** value missing **")
                    return
                else:
                    strArr[3] = strArr[3][1:i]
                if strArr[2] in obj.__dict__:
                    attrType = type(getattr(obj, strArr[2]))
                    strArr[3] = attrType(strArr[3])
                setattr(obj, strArr[2], strArr[3])
                obj.save()
            except Exception:
                print("** {} is not a valid value for {} **".format(
                    strArr[3], strArr[2]))
                print("** {} must be a(n) {} **".format(
                    strArr[2], attrType.__name__))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
