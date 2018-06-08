package FlowSensor

block HeaterElement
  parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium=Modelica.Thermal.FluidHeatFlow.Media.Medium()
    "Cooling medium"
    annotation(choicesAllMatching=true);
  parameter Modelica.SIunits.Temperature TAmb(displayUnit="degC")=293.15
    "Ambient temperature";

  //parameter Modelica.SIunits.Resistance R(start = 1);
  //parameter Modelica.SIunits.Temperature T_ref = 300.15 "Reference temperature";
  //parameter Modelica.SIunits.LinearTemperatureCoefficient alpha = 0;
  //  Modelica.Electrical.Analog.Basic.Resistor Resistor(useHeatPort = true);
  //  Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR1(R = 20);
  //  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor hC1(C = 0.0025, T(fixed = true, start = 300.15));
  //  Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_a heatPort(T(start=T), Q_flow=-LossPower)
  //extends Modelica.Electrical.Analog.Interfaces.OnePort;
  // Modelica.SIunits.Resistance R_actual;
  Modelica.Electrical.Analog.Basic.HeatingResistor heatingResistor1(useHeatPort = true)  annotation(
    Placement(visible = true, transformation(origin = {0, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Electrical.Analog.Interfaces.PositivePin p annotation(
    Placement(visible = true, transformation(origin = {-100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Electrical.Analog.Interfaces.NegativePin n annotation(
    Placement(visible = true, transformation(origin = {100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Components.HeatedPipe heatedPipe1(
    medium=medium,
    m=0.1,
    T0=TAmb,
    V_flowLaminar=0.1,
    dpLaminar(displayUnit="Pa") = 0.1,
    V_flowNominal=1,
    dpNominal(displayUnit="Pa") = 1,
    h_g=0,
    T0fixed=true
  )  annotation(
    Placement(visible = true, transformation(origin = {0, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Interfaces.FlowPort_a flowPort_a1 annotation(
    Placement(visible = true, transformation(origin = {-100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Interfaces.FlowPort_b flowPort_b1 annotation(
    Placement(visible = true, transformation(origin = {100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heatCapacitor1(C = 1, T(fixed = true))  annotation(
    Placement(visible = true, transformation(origin = {58, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
connect(flowPort_a1, heatedPipe1.flowPort_a) annotation(
    Line(points = {{-100, 40}, {-10, 40}}, color = {255, 0, 0}));
connect(heatedPipe1.flowPort_b, flowPort_b1) annotation(
    Line(points = {{10, 40}, {100, 40}}, color = {255, 0, 0}));
connect(heatingResistor1.heatPort, heatedPipe1.heatPort) annotation(
    Line(points = {{0, -50}, {0, -60}, {20, -60}, {20, 20}, {0, 20}, {0, 30}}, color = {191, 0, 0}));
connect(heatCapacitor1.port, heatedPipe1.heatPort) annotation(
    Line(points = {{58, 16}, {0, 16}, {0, 30}}, color = {191, 0, 0}));
  connect(heatingResistor1.p, p) annotation(
    Line(points = {{-10, -40}, {-100, -40}}, color = {0, 0, 255}));
  connect(heatingResistor1.n, n) annotation(
    Line(points = {{10, -40}, {100, -40}}, color = {0, 0, 255}));
/*
connect(n,Resistor.n);
connect(p,Resistor.p);
connect(heatPort,Resistor.heatPort);
*/
/*
R_actual = R * (1 + alpha * T_ref);
v = R_actual * i;
heatPort.Q_flow = -v * i;
*/
end HeaterElement;





  model HeaterTester
  parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium=Modelica.Thermal.FluidHeatFlow.Media.Medium()
      "Cooling medium"
      annotation(choicesAllMatching=true);
        parameter Modelica.SIunits.Temperature TAmb(displayUnit="degC")=293.15
      "Ambient temperature";
    FlowSensor.HeaterElement heaterElement1 annotation(
      Placement(visible = true, transformation(origin = {2, 0}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
    Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage1(V = 10) annotation(
      Placement(visible = true, transformation(origin = {6, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Electrical.Analog.Basic.Ground ground1 annotation(
      Placement(visible = true, transformation(origin = {44, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Sources.VolumeFlow volumeFlow1(
      medium=medium,
      m=0,
      T0=TAmb,
      useVolumeFlowInput=true,
      constantVolumeFlow=1
    )  annotation(
      Placement(visible = true, transformation(origin = {-38, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 1)  annotation(
      Placement(visible = true, transformation(origin = {-70, 4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient1(constantAmbientPressure = 100000, constantAmbientTemperature = 293.15)  annotation(
      Placement(visible = true, transformation(origin = {24, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient2(constantAmbientPressure = 100000, constantAmbientTemperature = 303.15)  annotation(
      Placement(visible = true, transformation(origin = {-58, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  equation
    connect(volumeFlow1.flowPort_a, ambient2.flowPort) annotation(
      Line(points = {{-48, -24}, {-86, -24}, {-86, -80}, {-68, -80}, {-68, -80}}, color = {255, 0, 0}));
    connect(heaterElement1.flowPort_b1, ambient1.flowPort) annotation(
      Line(points = {{12, -4}, {22, -4}, {22, -50}, {0, -50}, {0, -80}, {14, -80}, {14, -80}}, color = {255, 0, 0}));
    connect(volumeFlow1.flowPort_b, heaterElement1.flowPort_a1) annotation(
      Line(points = {{-28, -24}, {-20, -24}, {-20, -4}, {-8, -4}, {-8, -4}}, color = {255, 0, 0}));
    connect(const.y, volumeFlow1.volumeFlow) annotation(
      Line(points = {{-58, 4}, {-50, 4}, {-50, -8}, {-38, -8}, {-38, -14}, {-38, -14}}, color = {0, 0, 127}));
    connect(constantVoltage1.p, heaterElement1.p) annotation(
      Line(points = {{-4, 60}, {-40, 60}, {-40, 0}, {-8, 0}}, color = {0, 0, 255}));
    connect(constantVoltage1.n, heaterElement1.n) annotation(
      Line(points = {{16, 60}, {50, 60}, {50, 0}, {12, 0}}, color = {0, 0, 255}));
    connect(heaterElement1.n, ground1.p) annotation(
      Line(points = {{12, 0}, {44, 0}, {44, -38}}, color = {0, 0, 255}));
  end HeaterTester;

  model HeatedPipTester
    Modelica.Thermal.FluidHeatFlow.Components.HeatedPipe heatedPipe1 annotation(
      Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.VolumeFlow volumeFlow1 annotation(
      Placement(visible = true, transformation(origin = {-38, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  equation
    connect(volumeFlow1.flowPort_b, heatedPipe1.flowPort_a) annotation(
      Line(points = {{-28, 0}, {-10, 0}, {-10, 0}, {-10, 0}}, color = {255, 0, 0}));
  
  end HeatedPipTester;
  annotation(
    uses(Modelica(version = "3.2.2")));
end FlowSensor;
