#!/usr/bin/python3
""" It's Console Module """
import cmd
import sys
import re
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column, String


class HBNBCommand(cmd.Cmd):
    """ It's Contains the functionality for the HBNB console"""

    # So determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """It's Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """It's Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # It's scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # It's parse line left to right
            pline = line[:]  # parsed line

            # It's isolate <class name>
            _cls = pline[:pline.find('.')]

            # It's isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # It's if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """It's Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """It's Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """It's Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """It's Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """It's Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """It's Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """It's Create an object of any class"""
        pat = """(^\w+)((?:\s+\w+=[^\s]+)+)?"""
        mm = re.match(pat, args)
        args = [s for s in mm.groups() if s] if mm else []

        if not args:
            print("** class name missing **")
            return

        className = args[0]

        if className not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        kwargs = dict()
        if len(args) > 1:
            params = args[1].split(" ")
            params = [param for param in params if param]
            for param in params:
                [name, value] = param.split("=")
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                kwargs[name] = value

        newInstance = HBNBCommand.classes[className]()

        for attrName, attrValue in kwargs.items():
            setattr(newInstance, attrName, attrValue)

        newInstance.save()
        print(newInstance.id)

    def help_create(self):
        """ It's Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ It's Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # It's guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ It's Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ It's Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ It's Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ It's Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ It's Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """It's Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """It's Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # It's isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # It's class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # It's isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # So generate key from class and id
        key = c_name + "." + c_id

        # It's determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # So first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # It reforma kwarg into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # It's isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # So, if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # So, check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # It's if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # It's retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # So, iterate through attr names and values
        for i, att_name in enumerate(args):
            # So block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # So following item is value
                if not att_name:  # So check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # So check for att_value
                    print("** value missing **")
                    return
                # So type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # It's update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # So save updates to file

    def help_update(self):
        """ It's Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if _name_ == "__main__":
    HBNBCommand().cmdloop()
