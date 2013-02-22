#!/usr/bin/env python

import sys, os
import graphit
import argparse
import webbrowser
import yaml

def test_config():
  if not graphit.config.test_config():
    print "Config does not exist, please enter your information"
    sys.stdout.write("User ID: ")
    graphit.config.user_id = sys.stdin.readline().rstrip()
    sys.stdout.write("API Key: ")
    graphit.config.api_key = sys.stdin.readline().rstrip()
    graphit.config.save()

    
def main():
  parser = argparse.ArgumentParser(description='Graphit.io Shell Utility')
  subparsers = parser.add_subparsers(help='sub-command help', dest="command")

  #Config Parser for settings
  config = subparsers.add_parser('config', help='Config Global Settings')
  config.add_argument('--user_id', '-u', help='User ID (From Account Profile)')
  config.add_argument('--api_key', '-a', help='API Access Key (From Account Profile)')

  #Parser for creating news graphs
  new_graph = subparsers.add_parser('new', help='Create New Graph')
  new_graph.add_argument('--name', '-n', required=True, help='Name and title of the Graph')
  new_graph.add_argument('-x', '--x_label', help='Graph X Axis Label')
  new_graph.add_argument('-y', '--y_label', help='Graph Y Axis Label')

  new_point = subparsers.add_parser('add', help='Add data to existing graph')
  new_point.add_argument('-g', '--graphid', required=False, help='ID of Graph')
  new_point.add_argument('-x', '--x_value', required=True, help='Value of X')
  new_point.add_argument('-y', '--y_value', required=True, help='Value of Y')
  new_point.add_argument('-s', '--series', required=False, help='Graph Series Name')
  new_point.add_argument('-n', '--no_update', action='store_false', required=False, help='Do not update graph after insert')

  remove = subparsers.add_parser('remove', help='Remove data from graph')
  remove.add_argument('-g', '--graphid', required=False, help='ID of Graph')
  remove.add_argument('-l', '--lessthan', required=False, help='Select Data Less than this')
  remove.add_argument('-m', '--morethan', required=False, help='Select Data Greater than this')
  remove.add_argument('-n', '--no_update', action='store_false', required=False, help='Update graph after remove')

  update = subparsers.add_parser('update', help='Update Graph')
  update.add_argument('-g', '--graphid', required=False, help='ID of Graph')
  update.add_argument('-n', '--name', required=False, help='Update Graph Name')
  update.add_argument('-x', '--x_label', required=False, help='Update X Label')
  update.add_argument('-y', '--y_label', required=False, help='Update Y Label')

  use = subparsers.add_parser('use', help='Graph to use for subsequent actions')
  use.add_argument('-g', '--graphid', required=True, help='ID of Graph')
  
  del_graph = subparsers.add_parser('delete', help='Delete an existing graph')
  del_graph.add_argument('-g', '--graphid', required=True, help='ID of Graph')
  
  info = subparsers.add_parser('info', help='Display graph info')
  info.add_argument('-g', '--graphid', required=False, help='ID of Graph')

  open_graph = subparsers.add_parser('open', help='Open graph in default browser')
  open_graph.add_argument('-g', '--graphid', required=False, help='ID of Graph')

  list_graphs = subparsers.add_parser('list', help='List all Graphs')
    
  build = subparsers.add_parser('build', help='Build Data Set by adding data')
  build.add_argument('-g', '--graphid', required=False, help='ID of Graph')
  build.add_argument('-x', '--x_value', required=True, help='Value of X')
  build.add_argument('-y', '--y_value', required=True, help='Value of Y')
  build.add_argument('-s', '--series', required=False, help='Graph Series Name')

  send = subparsers.add_parser('send', help='Send Data Set')
  send.add_argument('-g', '--graphid', required=False, help='ID of Graph')
  send.add_argument('-n', '--no_update', action='store_false', required=False, help='Do not update graph after sending')
  

  
  args = parser.parse_args()
    
  if args.command == "config":
    if args.user_id:
        graphit.config.user_id = args.user_id
    if args.api_key:
        graphit.config.api_key = args.api_key
    if args.user_id or args.api_key:
        graphit.config.save()
    print "User ID: %s"%graphit.config.user_id
    print "API Key: %s"%graphit.config.api_key
  else:
    test_config()
  if args.command == "new":
    g = graphit.new_graph({"name":args.name, "x_label": args.x_label, "y_label": args.y_label})
    g.read()
    print "%s : %s"%(g._id, g.name)
    graphit.config.last_graph = g._id
    graphit.config.save()
  elif args.command == "delete":
    graphit.Graph(args.graphid).destroy()
  elif args.command == "add":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    g = graphit.Graph(g_id)
    g.add_datum(args.x_value, args.y_value,args.series,update=args.no_update)
    graphit.config.last_graph = g_id
    graphit.config.save()
  elif args.command == "list":
    for graph in graphit.list_graphs():
      print "%s : %s"%(graph['_id'], graph['name'])
  elif args.command == "update":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    g = graphit.Graph(g_id)
    g.update({"x_label": args.x_label, "y_label": args.y_label})
    graphit.config.last_graph = g_id
    graphit.config.save()
  elif args.command == "use":
    graphit.config.last_graph = args.graphid
    graphit.config.save()
  elif args.command == "remove":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    g = graphit.Graph(g_id)
    g.delete_data(less_than=args.lessthan, greater_than=args.morethan, update=args.no_update)
    graphit.config.last_graph = g_id
    graphit.config.save()
  elif args.command == "info":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    g = graphit.Graph(g_id)
    g.read()
    if g.name:
      print "Name: %s" % g.name
    print "ID: %s"%g._id
    print "URL: %s"%g.url()
    if g.x_label:
      print "X Label: %s"%g.x_label
    if g.y_label:
      print "Y Label: %s"%g.y_label
    if g.x_min != None:
      print "X Min: %f"%g.x_min
    if g.x_max != None:
      print "X Max: %f"%g.x_max
    if g.y_min != None:
      print "Y Min: %f"%g.y_min
    if g.y_max != None:
      print "Y Max: %f"%g.y_max
    if g.x_window_min != None:
      print "X Window Min: %f"%g.x_window_min
    if g.x_window_max != None:
      print "X Window Max: %f"%g.x_window_max
    if g.y_window_min != None:
      print "Y Window Min: %f"%g.y_window_min
    if g.y_window_max != None:
      print "Y Window Max: %f"%g.y_window_max
    if g.from_end != None:
      print "From end: %f"%g.from_end
    if g.from_start != None:
      print "From Start: %f"%g.from_start
    if g.samples != None:
      print "Samples: %d"%g.samples
  elif args.command == "open":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    g = graphit.Graph(g_id)
    webbrowser.open(g.url())
  elif args.command == "build":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    ds_file = open(os.path.expanduser("~/.graphit_data_%s"%g_id), "a+")
    ds_file.write(yaml.dump(graphit.data.Datum(args.x_value, args.y_value, args.series)))
    ds_file.close()
    graphit.config.last_graph = g_id
    graphit.config.save()

  elif args.command == "send":
    g_id = graphit.util.working_graph(args)
    if not g_id:
      print "No graph specified"
      return
    ds_file = open(os.path.expanduser("~/.graphit_data_%s"%g_id))
    ds = graphit.data.DataSet()
    for datum in ds_file:
        datum = yaml.load(datum)
        ds.add_datum(datum)
    ds_file.close()
    g = graphit.Graph(g_id)
    g.add_data_set(ds, update=args.no_update)      
    os.unlink(os.path.expanduser("~/.graphit_data_%s"%g_id))
    graphit.config.last_graph = g_id
    graphit.config.save()

        

    
          


      


if __name__ == "__main__":
  main()
