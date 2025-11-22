import Sofa
import SofaRuntime
import os

meshpath = os.path.dirname(os.path.abspath(__file__)) + '/mesh/'

def main():
    # Make sure to load all necessary libraries
    SofaRuntime.importPlugin("Sofa.Component.StateContainer")

    # Call the above function to create the scene graph
    root = Sofa.Core.Node("root")
    createScene(root)

    # Once defined, initialization of the scene graph
    Sofa.Simulation.init(root)


# Function called when the scene graph is being created
def createScene(root):

    root.addObject('RequiredPlugin', pluginName='CGALPlugin')

    node = root.addChild('node')

    node.addObject('MeshOBJLoader', name="loader",filename=meshpath+'/class/sphere0_c.obj')
    node.addObject('MeshGenerationFromPolyhedron', name="MeshGenerator", inputPoints='@loader.position', inputTriangles='@loader.triangles', inputQuads='@loader.quads', 
                   drawTetras='1', facetSize="10", facetApproximation="10", cellRatio="10", cellSize="1" )
    node.addObject('MechanicalObject', name="dofs", position="@MeshGenerator.outputPoints")
    node.addObject('TetrahedronSetTopologyContainer', name="topo", tetrahedra="@MeshGenerator.outputTetras")
    node.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo", drawTetrahedra="1", drawScaleTetrahedra="1")
    node.addObject('VTKExporter', filename='sphere', edges='0', tetras='1', exportAtBegin='1')
        
    return root

