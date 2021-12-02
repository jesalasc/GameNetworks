
import networkx as nx
from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, EdgesAndLinkedNodes, NodesAndLinkedEdges, LabelSet
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
import numpy as np

class Networks_Game:
    
    def __init__(self, students, Network = "Graph.txt", Round = 0):
        self.round = Round
        self.students = students
        self.pending_changes = {}
        self.game_size = len(students)
        for student in students:
            self.pending_changes[student] = True
        self.changes_made = 0
        #if Network == None:
        #    self.graph = nx.Graph()
        #    
        #else:
        self.graph = nx.read_edgelist(Network, create_using=nx.Graph())
        self.graph.add_nodes_from(self.students)
            
        
        
    def new_change(self, student, add1, add2, rem = None):
        decided = student.decided
        if add1 != None or add2 != None:
            if add1 != add2 and (not decided):
                student.add_changes(add1, add2, rem)
                self.pending_changes[student.id] = False
                self.changes_made+=1
                return True,"Changes added."
            elif add1 == add2:
                return False,"New connections must be different."
            else:
                return False, "You already made changes."
        else:
            if (not decided):
                student.add_changes(add1, add2, rem)
                self.pending_changes[student.id] = False
                self.changes_made+=1
                return True,"Changes added."
            else:
                return False, "You already made changes."   
            
    def apply_changes(self, students):
        
        if self.round > 0:
            to_add = []
            to_remove = []
            for student in students:
                if student.add1 != None:
                    to_add.append((student.id ,student.add1))
                if student.add2 != None:
                    to_add.append((student.id, student.add2))
                if student.rem != None:
                    to_remove.append((student.id, student.rem))
                
                self.pending_changes[student.id] = False
            
            missing_students = [x for x in self.students if self.pending_changes[x]]
           
            for ID in missing_students:
                
                unconnected = self.unconnectedOF(ID)
                connected = self.connectionsOF(ID)
                if len(unconnected)>0:
                    add1 = np.random.choice(unconnected)
                    unconnected.remove(add1)
                    to_add.append((ID, add1))
                if len(unconnected)>0:
                    add2 = np.random.choice(unconnected) 
                    to_add.append((ID, add2))
                
                if len(connected)>0:
                    rem = np.random.choice(connected)
                    to_remove.append((ID, rem))
                
            
            self.graph.remove_edges_from(to_remove)
            self.graph.add_edges_from(to_add)
            self.changes_made = 0
            self.round += 1
            return True
            
        elif self.round == 0:
            to_add = []
            
            for student in students:
                if student.add1 != None:
                    to_add.append((student.id ,student.add1))
                if student.add2 != None:
                    to_add.append((student.id, student.add2))
            
            missing_students = [x for x in self.students if self.pending_changes[x]]
           
            for ID in missing_students:
                
                unconnected = self.unconnectedOF(ID)
                connected = self.connectionsOF(ID)
                if len(unconnected)>0:
                    add1 = np.random.choice(unconnected)
                    unconnected.remove(add1)
                    to_add.append((ID, add1))
                if len(unconnected)>0:
                    add2 = np.random.choice(unconnected) 
                    to_add.append((ID, add2))
                
                
            self.graph.add_edges_from(to_add)
            self.changes_made = 0
            self.round += 1
            return True
        
        else:
            
            return False
    
    def connectionsOF(self, studentID):
        return list(self.graph.neighbors(studentID))
    
    def unconnectedOF(self, studentID):
        connected = self.connectionsOF(studentID)
        connected.append(studentID)
        return [x for x in self.students if (x not in connected)]
    
    def save_network(self, path):
        
        with open(path, "wb") as f:
            nx.readwrite.edgelist.write_edgelist(self.graph, f)
            f.close()
        return True
    
    def compute_ranking(self):
        degree = nx.algorithms.centrality.degree_centrality(self.graph)
        clustering = nx.algorithms.cluster.clustering(self.graph)
        between = nx.algorithms.centrality.betweenness_centrality(self.graph, normalized=True)
        
        nx.set_node_attributes(self.graph, name='degree', values=degree)
        nx.set_node_attributes(self.graph, name='clustering', values=clustering)
        nx.set_node_attributes(self.graph, name='BTC', values=between)
        
        return True
    
    def visualize(self):
        #adjusted degree for visualization
        number_to_adjust_by = 30
        adjusted_node_size = dict([(node, degree+number_to_adjust_by) for node, degree in self.graph.degree()])
        nx.set_node_attributes(self.graph, name='adjusted_node_size', values=adjusted_node_size)
       
        #Choose colors for node and edge highlighting
        node_highlight_color = 'blue'
        edge_highlight_color = 'red'
        
        #Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
        size_by_this_attribute = 'adjusted_node_size'
        #color_by_this_attribute = 'modularity_color'
        
        #Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
        #color_palette = Blues8
        
        #Choose a title!
        title = 'Game of Networks Round '+ str(self.round)
        
        #Establish which categories will appear when hovering over each node
        HOVER_TOOLTIPS = [
               ("Student ID", "@index"),
                ("Degree", "@degree"),
                 ("Clustering coefficient", "@clustering"),
                ("Betwenness Centrality", "@BTC"),
        ]
        
        #Create a plot — set dimensions, toolbar, and title
        plot = figure(tooltips = HOVER_TOOLTIPS,
                      tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                    x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)
        
        #Create a network graph object
        # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
        network_graph = from_networkx(self.graph, nx.spring_layout, scale=10, center=(0, 0))
        
        #Set node sizes and colors according to node degree (color as category from attribute)
        
        #network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)
        network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color="#3288bd")

        #Set node highlight colors
        network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
        network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
        
        #Set edge opacity and width
        network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.3, line_width=1)
        #Set edge highlight colors
        network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
        network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
        
        #Highlight nodes and edges
        network_graph.selection_policy = NodesAndLinkedEdges()
        network_graph.inspection_policy = NodesAndLinkedEdges()
        
        plot.renderers.append(network_graph)
        
        #Add Labels
        x, y = zip(*network_graph.layout_provider.graph_layout.values())
        node_labels = list(self.graph.nodes())
        source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
        labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px', background_fill_alpha=.7)
        plot.renderers.append(labels)
        
        
        #save(plot, filename=f"{title}.html")

        return plot
        
class Student:
    
    def __init__(self, id):
        self.id = id
        self.add1 = None
        self.add2 = None
        self.rem = None
        self.decided = False
        
    def add_changes(self, add1, add2, rem= None):
        if not self.decided:
            self.add1 = add1
            self.add2 = add2
            self.rem = rem
            self.decided = True
            return True
        return False
    
    def reset_changes(self):
        self.add1 = None
        self.add2 = None
        self.rem = None
        self.decided = False
        
        
        
        