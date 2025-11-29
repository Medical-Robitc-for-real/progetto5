import Sofa
# import SofaRuntime
# import Sofa.Gui
# custom python controller
from Controller import ThreeInstrumentsController

def createScene(root):
    # Parameters:
    straight_length = [95.0, 115.0, 145.0] # [mm]
    curved_length = [30.0, 40.0, 55.0] # [mm]
    tube_radius = [0.85, 0.75, 0.65] # [mm]
    radius_curvature = [90.0, 100.0, 115.0] # [mm]

    # Root Node
    root.dt = 0.05
    root.gravity = (0, 0, 0)

    required_plugins = [
        "BeamAdapter",
        "Sofa.Component.Constraint.Projective",
        "Sofa.Component.LinearSolver.Direct",
        "Sofa.Component.Mapping.Linear",
        "Sofa.Component.ODESolver.Backward",
        "Sofa.Component.SolidMechanics.Spring",
        "Sofa.Component.StateContainer",
        "Sofa.Component.Topology.Container.Dynamic",
        "Sofa.Component.Topology.Container.Grid",
        "Sofa.Component.Topology.Mapping",
        "Sofa.Component.Visual",
        "Sofa.GL.Component.Rendering3D",
        "Sofa.Component.Constraint.Lagrangian", # added for terminal
        "Sofa.GL.Component.Shader",
    ]

    for plugin in required_plugins:
        root.addObject("RequiredPlugin", name=plugin)

    # Visual Style
    root.addObject('VisualStyle', displayFlags='showVisualModels ' \
                                    'showBehaviorModels ' \
                                    'showCollisionModels ' \
                                    'hideMappings ' \
                                    'hideForceFields')

    # Default Animation and Visual Loops
    root.addObject('DefaultAnimationLoop')
    root.addObject('DefaultVisualManagerLoop')

    root.addObject('GenericConstraintSolver',
               name='ConstraintSolver',
               computeConstraintForces="1",
               tolerance='1e-10',
               maxIterations='1000')



    #----> 1. Catheter
    # RodStraightSection and RodSpireSection for Catheter
    topoLines_cath = root.addChild('topoLines_cath')
    topoLines_cath.addObject('RodStraightSection', 
                             name="CathStraightSection", 
                             youngModulus=10000, 
                             massDensity=0.00000155, 
                             nbEdgesCollis=50, 
                             nbEdgesVisu=300, 
                             length=straight_length[0], 
                             radius=tube_radius[0],
                             poissonRatio=0.3)
    
    topoLines_cath.addObject('RodSpireSection', 
                             name="CathSpireSection", 
                             youngModulus=10000, 
                             massDensity=0.00000155, 
                             nbEdgesCollis=10, 
                             nbEdgesVisu=300, 
                             length=curved_length[0], 
                             spireDiameter=2*radius_curvature[0], 
                             spireHeight=0.0, 
                             radius=tube_radius[0],
                             poissonRatio=0.3)
    
    # WireRestShape for Catheter: condizione di riposo
    topoLines_cath.addObject('WireRestShape', 
                             name='catheterRestShape', 
                             template="Rigid3d",
                             wireMaterials="@CathStraightSection @CathSpireSection")
    
    # Mesh and Geometry for Catheter
    topoLines_cath.addObject('EdgeSetTopologyContainer', name='meshLinesCath')
    topoLines_cath.addObject('EdgeSetTopologyModifier', name='Modifier')
    topoLines_cath.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    topoLines_cath.addObject('MechanicalObject', name='dofTopo1', template='Rigid3d', position="0 0 0 0 0 0 1")
    # topoLines_cath.addObject('UniformMass', totalMass=0.1)

    #----> 2. Guidewire
    # RodStraightSection and RodSpireSection for Guidewire
    topo_lines_guide = root.addChild('topoLines_guide')
    topo_lines_guide.addObject('RodStraightSection',
                               name="GuideStraightSection", 
                               youngModulus=10000, 
                               massDensity=0.00000155,  
                               nbEdgesCollis=50, 
                               nbEdgesVisu=300, 
                               length=straight_length[1], 
                               radius=tube_radius[1],
                               poissonRatio=0.3)
    
    topo_lines_guide.addObject('RodSpireSection', 
                               name="GuideSpireSection", 
                               youngModulus=10000, 
                               massDensity=0.00000155,
                               nbEdgesCollis=10, 
                               nbEdgesVisu=300, 
                               length=curved_length[1], 
                               spireDiameter=2*radius_curvature[1], 
                               spireHeight=0.0, 
                               radius=tube_radius[1],
                               poissonRatio=0.3)
    
    # WireRestShape for Guidewire
    topo_lines_guide.addObject('WireRestShape', 
                               name='GuideRestShape', 
                               template="Rigid3d",
                               wireMaterials="@GuideStraightSection @GuideSpireSection")
    
    # Mesh and Geometry for Guidewire
    topo_lines_guide.addObject('EdgeSetTopologyContainer', name='meshLinesGuide')
    topo_lines_guide.addObject('EdgeSetTopologyModifier', name='Modifier')
    topo_lines_guide.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    topo_lines_guide.addObject('MechanicalObject', name='dofTopo2', template='Rigid3d', position="0 0 0 0 0 0 1")
    # topo_lines_guide.addObject('UniformMass', totalMass=0.1)
    
    #----> 3. Coils
    # RodStraightSection and RodSpireSection for Coils
    straight_section_coils = root.addChild('topoLines_coils')
    straight_section_coils.addObject('RodStraightSection',
                                     name="CoilStraightSection", 
                                     youngModulus=168000, 
                                     massDensity=0.000021,  
                                     nbEdgesCollis=50, 
                                     nbEdgesVisu=300, 
                                     length=straight_length[2], 
                                     radius=tube_radius[2],
                                     poissonRatio=0.3)
    
    straight_section_coils.addObject('RodSpireSection', 
                                     name="CoilSpireSection", 
                                     youngModulus=168000, 
                                     massDensity=0.000021,
                                     nbEdgesCollis=10, 
                                     nbEdgesVisu=300, 
                                     length=curved_length[2], 
                                     spireDiameter=2*radius_curvature[2], 
                                     spireHeight=0.0, 
                                     radius=tube_radius[2],
                                     poissonRatio=0.3)
    
    # WireRestShape for Coils
    straight_section_coils.addObject('WireRestShape', 
                                     name='CoilRestShape', 
                                     template="Rigid3d",
                                     wireMaterials="@CoilStraightSection @CoilSpireSection")
    
    # Mesh and Geometry for Coils
    straight_section_coils.addObject('EdgeSetTopologyContainer', name='meshLinesCoils')
    straight_section_coils.addObject('EdgeSetTopologyModifier', name='Modifier')
    straight_section_coils.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    straight_section_coils.addObject('MechanicalObject', name='dofTopo3', template='Rigid3d', position="0 0 0 0 0 0 1")
    # straight_section_coils.addObject('UniformMass', totalMass=0.1)

    # RefStartingPos = root.addChild('RefStartingPos')
    # RefStartingPos.addObject('MechanicalObject', name="ReferencePos", template="Rigid3d", position="-3 1.5 0.3  1 0 0 0")    

    # ----> 4. Combine the 3 instruments
    instrument_combined = root.addChild("InstrumentCombined")
    instrument_combined.addObject('EulerImplicitSolver', 
                                  rayleighStiffness=0.2, 
                                  rayleighMass=0.03, 
                                  printLog=False)
    instrument_combined.addObject('BTDLinearSolver')
    instrument_combined.addObject('RegularGridTopology', 
                                  name='meshLinesCombined', 
                                  nx=181, ny=1, nz=1)
    instrument_combined.addObject('MechanicalObject', 
                                  template='Rigid3d', 
                                  name='DOFs')

    # Wire Interpolation and Force Fields
    instrument_combined.addObject("InterventionalRadiologyController",
               template="Rigid3d",
               name="IRController",
               printLog="0",
               xtip="0 0 0",
               step="1",
               rotationInstrument="0 0 0",
               controlledInstrument="0",
               startingPos="0 0 0 0 0 0 1",
               speed="0",
               instruments="InterpolCatheter InterpolGuide InterpolCoils")
    
    instrument_combined.addObject('WireBeamInterpolation', 
                                  name="InterpolCatheter", 
                                  WireRestShape="@../topoLines_cath/catheterRestShape",
                                  printLog=False)
    instrument_combined.addObject('AdaptiveBeamForceFieldAndMass',
                                  name="CatheterForceField", 
                                  interpolation="@InterpolCatheter",
                                  printLog=False)
    
    instrument_combined.addObject('WireBeamInterpolation',
                                  name="InterpolGuide", 
                                  WireRestShape="@../topoLines_guide/GuideRestShape",
                                  printLog=False)
    instrument_combined.addObject('AdaptiveBeamForceFieldAndMass',
                                  name="GuideForceField", 
                                  interpolation="@InterpolGuide",
                                  printLog=False)
    
    instrument_combined.addObject('WireBeamInterpolation',
                                  name="InterpolCoils", 
                                  WireRestShape="@../topoLines_coils/CoilRestShape",
                                  printLog=False)
    instrument_combined.addObject('AdaptiveBeamForceFieldAndMass',
                                  name="CoilsForceField", 
                                  interpolation="@InterpolCoils",
                                  printLog=False)
    
    
    instrument_combined.addObject('LinearSolverConstraintCorrection', printLog=False, wire_optimization="true")

    # Aggiunta del controller
    instrument_combined.addObject(ThreeInstrumentsController(instrument_combined.IRController))

    # Simulazione tempi vs azioni
    # instrument_combined.addObject("BeamAdapterActionController",
    #            name="AController",
    #            interventionController="@IRController",
    #            writeMode="0",
    #            timeSteps="9.1 17.1 17.55 18.05 18.6 19.05 19.55 20.05 20.5 21 21.45 21.9 22.65 23.1 23.55 24.05 24.55 25 25.45 25.95 26.4 27.1 27.55 28.05 28.55 29 29.5 29.95 30.4 30.9 31.4 31.85 32.35 33.05 33.5 34 34.45 34.9 35.4 35.85 36.35 36.8 37.25 37.7 38.2 38.65 39.4 39.85 40.3 40.7 41.2 41.65 42.1 42.55 43 43.4 44.1 44.55 45 45.45 45.9 46.3 46.75 47.2 47.65 48.1 48.55 49 49.65 50.1 50.5 50.9 51.35 51.75 52.2 52.6 53.05 53.5 53.95 54.4 54.85 55.5 55.9 59.1 66.15 66.6 67.05 67.45 67.9 68.35 68.8 69.25 69.65 70.1 70.55 71.2 71.6 72.05 72.5 72.95 73.4 77.6 81.9 87.4 87.75 88.1 88.45 88.75 89.1 89.45 89.75 90.1 90.6 90.9 91.25 91.6 91.95 92.3 92.6 92.95 93.25 93.6 93.95 94.25 94.6 94.95 95.4 95.75 96.1 96.4 96.75 97.05 97.35 97.7 98.05 98.4 98.7 99.15 99.5 99.8 100.15 100.45 100.75 101.1 101.4 101.75 102.05 102.55 102.85 103.2 103.5 103.8 104.1 104.4 104.75 105.05 105.4 105.7 106 106.45 106.75 107.1 107.4 107.7 108 108.35 108.65 108.95 109.25 109.55 110 110.3 110.6 110.9 111.2 111.45 111.75 112.05 112.35 112.65 113.1 113.35 113.65 113.95 114.2 114.5 114.8 115.1 115.35 115.65 116.1 116.35 125.8 128.2 131.6 131.8 132 132.25 132.45 132.65 132.85 133.05 133.3 133.5 133.8 134 134.2 134.4 134.6 134.8 135 135.2 135.4 135.6 135.8 136 136.3 136.5 136.75 136.95 137.15 137.35 137.5 137.7 137.9 138.15 138.3 138.6 138.85 139 139.2 139.4 139.6 139.8 140 140.15 140.35 140.55 140.75 140.95 141.25 141.45 141.65 141.85 142.05 142.25 142.45 142.65 142.85 143.05 143.25 143.45 143.65 143.85 144.15 144.3 144.5 144.7 144.9 145.1 145.3 145.45 145.65 145.95 146.1 146.3 146.5 146.7 146.9 147.1 147.25 147.45 147.65 147.85 148.05 148.25 148.4 148.7 148.9 149.1 149.25 149.45 149.65 149.85 150 150.2 150.35 150.55 150.75 150.9 151.05 151.3 151.45 151.6 151.8 151.95 152.1 152.25 152.4 152.65 152.8 153 153.15 153.3 153.45 153.6 153.75 153.9 154.1 154.25 154.4 154.6 154.75 154.9 155.1 155.25 155.4 155.55 155.7 155.85 156 156.15 156.4 156.55 156.7 156.85 157 157.15 157.3 157.45 157.6 157.75 157.9 158.05 159 160.9 163.4 163.55 163.7 163.85 164.1 164.25 164.4 164.55 164.75 164.9 165.05 165.2 165.35 165.5 165.65 165.8 165.95 166.15 166.35 166.5 166.7 166.85 167 167.15 167.3 167.45 167.65 167.8 167.95 168.1 168.25 168.45 168.6 168.8 169 169.15 169.3 169.45 169.6 169.8 169.95 170.1 170.25 170.4 170.55 170.7 170.95 171.1 171.25 171.4 171.55 171.75 171.9 172.05 172.2 172.45 172.6 172.75 172.9 173.1 173.25 185.8",
    #            actions="1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 9 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 10 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1")

    # Fissa il primo nodo dell'assieme
    instrument_combined.addObject("FixedProjectiveConstraint",
               name="FixedConstraint",
               indices="0")
    # queste molle mantengono fermo l'estremo iniziale degli strumenti. Questo evita che i tubi vadano via o "scorrano" se non si vuole
    instrument_combined.addObject("RestShapeSpringsForceField",
               points="@IRController.indexFirstNode",
               stiffness="1e8",
               angularStiffness="1e8")


    # VISUALIZATION NODES
    # ------------------- Catheter Visu ------------------------
    visuCath = instrument_combined.addChild("VisuCatheter")
    visuCath.addObject("MechanicalObject", name="Quads")
    visuCath.addObject("QuadSetTopologyContainer", name="ContainerCath")
    visuCath.addObject("QuadSetTopologyModifier", name="Modifier")
    visuCath.addObject("QuadSetGeometryAlgorithms",
                       name="GeomAlgo", template="Vec3d")
    visuCath.addObject("Edge2QuadTopologicalMapping",
                       nbPointsOnEachCircle=10, radius=tube_radius[0],
                       input="@../../topoLines_cath/meshLinesCath",
                       output="@ContainerCath", flipNormals=True, printLog=False)
    visuCath.addObject("AdaptiveBeamMapping",
                       name="VisuMapCath",
                       useCurvAbs=True, printLog=False,
                       interpolation="@../InterpolCatheter",
                       isMechanical=False)
    cathGL = visuCath.addChild("VisuOgl")
    cathGL.addObject("OglModel", name="Visual",
                     color="0 1 1", #1 0 0
                     scale3d="1.0 1.0 1.0")
    cathGL.addObject("IdentityMapping",
                     input="@../Quads", output="@Visual")
    # ------------------- Guide Visu ------------------------
    visuGuide = instrument_combined.addChild("VisuGuide")
    visuGuide.addObject("MechanicalObject", name="Quads")
    visuGuide.addObject("QuadSetTopologyContainer", name="ContainerGuide")
    visuGuide.addObject("QuadSetTopologyModifier", name="Modifier")
    visuGuide.addObject("QuadSetGeometryAlgorithms",
                        name="GeomAlgo", template="Vec3d")
    visuGuide.addObject("Edge2QuadTopologicalMapping",
                        nbPointsOnEachCircle=10, radius=tube_radius[1],
                        input="@../../topoLines_guide/meshLinesGuide",
                        output="@ContainerGuide", flipNormals=True, printLog=False)
    visuGuide.addObject("AdaptiveBeamMapping",
                        name="visuMapGuide",
                        useCurvAbs=True, printLog=False,
                        interpolation="@../InterpolGuide",
                        isMechanical=False)
    guideGL = visuGuide.addChild("VisuOgl")
    guideGL.addObject("OglModel", name="Visual",
                      color="1 1 0", # 0 1 0
                      scale3d="0.9 0.9 0.9")
    guideGL.addObject("IdentityMapping",
                      input="@../Quads", output="@Visual")
    # ------------------- Coils Visu ------------------------
    visuCoils = instrument_combined.addChild("VisuCoils")
    visuCoils.addObject("MechanicalObject", name="Quads")
    visuCoils.addObject("QuadSetTopologyContainer", name="ContainerCoils")
    visuCoils.addObject("QuadSetTopologyModifier", name="Modifier")
    visuCoils.addObject("QuadSetGeometryAlgorithms",
                        name="GeomAlgo", template="Vec3d")
    visuCoils.addObject("Edge2QuadTopologicalMapping",
                        nbPointsOnEachCircle=10, radius=tube_radius[2],
                        input="@../../topoLines_coils/meshLinesCoils",
                        output="@ContainerCoils",
                        flipNormals=True, printLog=False)
    visuCoils.addObject("AdaptiveBeamMapping",
                        name="visuMapCoils",
                        useCurvAbs=True, printLog=False,
                        interpolation="@../InterpolCoils",
                        isMechanical=False)
    coilsGL = visuCoils.addChild("VisuOgl")
    coilsGL.addObject("OglModel", name="Visual",
                      color="0 0 1",
                      scale3d="0.8 0.8 0.8")
    coilsGL.addObject("IdentityMapping",
                      input="@../Quads", output="@Visual")


    # Directional Light
    root.addObject('LightManager')
    light = root.addChild("light")
    light.addObject('DirectionalLight', name="dirLight", direction=[0, 1, 0])

    # Return the root node
    return root


# def main(): # non mostra la gui di SOFA se eseguito da terminale
#     root = Sofa.Core.Node("root")
#     createScene(root)
#     Sofa.Simulation.init(root)

#     Sofa.Gui.GUIManager.Init('myscene', 'qglviewer')
#     Sofa.Gui.GUIManager.createGUI(root, __file__)
#     Sofa.Gui.GUIManager.SetDimension(1080, 1080)
#     Sofa.Gui.GUIManager.MainLoop(root)
#     Sofa.Gui.GUIManager.closeGUI()



# Per eseguirlo via python3 3instruments.py aggiungi le seguenti:
# import subprocess
# import os

# def main():
#     scene_file = "/home/emanuele/SOFA/v25.06.00/Techical project/3instruments.py"

#     # fai partire runSofa esattamente con la tua scena Python
#     subprocess.run(["runSofa", scene_file])

# if __name__ == "__main__":
#     main()
