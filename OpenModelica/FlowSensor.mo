package FlowSensor
  block HeaterElement
    parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium = Modelica.Thermal.FluidHeatFlow.Media.Medium() "Cooling medium" annotation(
      choicesAllMatching = true);
    parameter Modelica.SIunits.Temperature TAmb(displayUnit = "degC") = 293.15 "Ambient temperature";
    output Modelica.SIunits.Temperature T_a "Temperature at flowPort_a";
    output Modelica.SIunits.Temperature T_b "Temperature at flowPort_b";
    //parameter Modelica.SIunits.Resistance R(start = 1);
    //parameter Modelica.SIunits.Temperature T_ref = 300.15 "Reference temperature";
    //parameter Modelica.SIunits.LinearTemperatureCoefficient alpha = 0;
    //  Modelica.Electrical.Analog.Basic.Resistor Resistor(useHeatPort = true);
    //  Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR1(R = 20);
    //  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor hC1(C = 0.0025, T(fixed = true, start = 300.15));
    //  Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_a heatPort(T(start=T), Q_flow=-LossPower)
    //extends Modelica.Electrical.Analog.Interfaces.OnePort;
    // Modelica.SIunits.Resistance R_actual;
    Modelica.Electrical.Analog.Basic.HeatingResistor heatingResistor1(useHeatPort = true) annotation(
      Placement(visible = true, transformation(origin = {0, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Electrical.Analog.Interfaces.PositivePin p annotation(
      Placement(visible = true, transformation(origin = {-100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Electrical.Analog.Interfaces.NegativePin n annotation(
      Placement(visible = true, transformation(origin = {100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {100, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Components.HeatedPipe heatedPipe1(medium = medium, m = 0.1, T0 = TAmb, V_flowLaminar = 0.1, dpLaminar(displayUnit = "Pa") = 0.1, V_flowNominal = 1, dpNominal(displayUnit = "Pa") = 1, h_g = 0, T0fixed = true) annotation(
      Placement(visible = true, transformation(origin = {0, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Interfaces.FlowPort_a flowPort_a1(medium = medium) annotation(
      Placement(visible = true, transformation(origin = {-100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Interfaces.FlowPort_b flowPort_b1(medium = medium) annotation(
      Placement(visible = true, transformation(origin = {100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {100, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  equation
    connect(heatingResistor1.heatPort, heatedPipe1.heatPort) annotation(
      Line(points = {{0, -50}, {0, -50}, {0, -60}, {20, -60}, {20, 20}, {0, 20}, {0, 30}, {0, 30}}, color = {191, 0, 0}));
    connect(flowPort_a1, heatedPipe1.flowPort_a) annotation(
      Line(points = {{-100, 40}, {-10, 40}}, color = {255, 0, 0}));
    connect(heatedPipe1.flowPort_b, flowPort_b1) annotation(
      Line(points = {{10, 40}, {100, 40}}, color = {255, 0, 0}));
    connect(heatingResistor1.p, p) annotation(
      Line(points = {{-10, -40}, {-100, -40}}, color = {0, 0, 255}));
    connect(heatingResistor1.n, n) annotation(
      Line(points = {{10, -40}, {100, -40}}, color = {0, 0, 255}));
    T_a=flowPort_a1.h/medium.cp;
    T_b=flowPort_b1.h/medium.cp;
    
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
    parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium = Modelica.Thermal.FluidHeatFlow.Media.Medium() "Cooling medium" annotation(
      choicesAllMatching = true);
    parameter Modelica.SIunits.Temperature TAmb(displayUnit = "degC") = 293.15 "Ambient temperature";
  Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient1 annotation(
      Placement(visible = true, transformation(origin = {-72, -38}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.VolumeFlow volumeFlow1
     annotation(
      Placement(visible = true, transformation(origin = {-24, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient2 annotation(
      Placement(visible = true, transformation(origin = {74, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  FlowSensor.HeaterElement heaterElement1 annotation(
      Placement(visible = true, transformation(origin = {16, 32}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage1 annotation(
      Placement(visible = true, transformation(origin = {14, 84}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Electrical.Analog.Basic.Ground ground1 annotation(
      Placement(visible = true, transformation(origin = {70, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 1e-3)  annotation(
      Placement(visible = true, transformation(origin = {-66, 8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  equation
    connect(volumeFlow1.volumeFlow, const.y) annotation(
      Line(points = {{-24, -30}, {-24, -30}, {-24, 8}, {-54, 8}, {-54, 8}}, color = {0, 0, 127}));
    connect(constantVoltage1.p, heaterElement1.p) annotation(
      Line(points = {{4, 84}, {-8, 84}, {-8, 36}, {6, 36}, {6, 36}}, color = {0, 0, 255}));
    connect(heaterElement1.n, ground1.p) annotation(
      Line(points = {{26, 36}, {70, 36}, {70, 36}, {70, 36}}, color = {0, 0, 255}));
    connect(constantVoltage1.n, ground1.p) annotation(
      Line(points = {{24, 84}, {70, 84}, {70, 36}, {70, 36}}, color = {0, 0, 255}));
    connect(heaterElement1.flowPort_b1, ambient2.flowPort) annotation(
      Line(points = {{26, 28}, {40, 28}, {40, -40}, {64, -40}, {64, -40}}, color = {255, 0, 0}));
    connect(volumeFlow1.flowPort_b, heaterElement1.flowPort_a1) annotation(
      Line(points = {{-14, -40}, {-8, -40}, {-8, 28}, {6, 28}, {6, 28}}, color = {255, 0, 0}));
    connect(ambient1.flowPort, volumeFlow1.flowPort_a) annotation(
      Line(points = {{-62, -38}, {-34, -38}, {-34, -40}, {-34, -40}}, color = {255, 0, 0}));
  end HeaterTester;




  model HeatedPipTester
    parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium = Modelica.Thermal.FluidHeatFlow.Media.Medium() "Cooling medium" annotation(
      choicesAllMatching = true);
    parameter Modelica.SIunits.Temperature TAmb(displayUnit = "degC") = 293.15 "Ambient temperature";
  Modelica.Thermal.FluidHeatFlow.Sources.VolumeFlow volumeFlow1 annotation(
      Placement(visible = true, transformation(origin = {-38, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Components.HeatedPipe heatedPipe1(medium = medium, T0 = TAmb, m = 0.1, V_flowLaminar = 0.1, dpLaminar(displayUnit = "Pa") = 0.1, V_flowNominal = 1, dpNominal(displayUnit = "Pa") = 1, h_g = 0, T0fixed = true) annotation(
      Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient1 annotation(
      Placement(visible = true, transformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient2 annotation(
      Placement(visible = true, transformation(origin = {-70, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
  equation
    connect(ambient2.flowPort, volumeFlow1.flowPort_a) annotation(
      Line(points = {{-60, 0}, {-48, 0}, {-48, 0}, {-48, 0}}, color = {255, 0, 0}));
    connect(volumeFlow1.flowPort_b, heatedPipe1.flowPort_a) annotation(
      Line(points = {{-28, 0}, {-10, 0}, {-10, 0}, {-10, 0}}, color = {255, 0, 0}));
    connect(heatedPipe1.flowPort_b, ambient1.flowPort) annotation(
      Line(points = {{10, 0}, {46, 0}, {46, 0}, {46, 0}}, color = {255, 0, 0}));
  end HeatedPipTester;

  model HeatedPipeTester
    parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium = Modelica.Thermal.FluidHeatFlow.Media.Medium() "Cooling medium" annotation(
      choicesAllMatching = true);
    parameter Modelica.SIunits.Temperature TAmb(displayUnit = "degC") = 293.15 "Ambient temperature";
    Modelica.Thermal.FluidHeatFlow.Components.HeatedPipe heatedPipe1(medium = medium, T0 = TAmb, m = 0.1, V_flowLaminar = 0.1, dpLaminar(displayUnit = "Pa") = 0.1, V_flowNominal = 1, dpNominal(displayUnit = "Pa") = 1, h_g = 0, T0fixed = true) annotation(
      Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.VolumeFlow volumeFlow1 annotation(
      Placement(visible = true, transformation(origin = {-38, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient1 annotation(
      Placement(visible = true, transformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient2 annotation(
      Placement(visible = true, transformation(origin = {-70, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
  equation
    connect(ambient2.flowPort, volumeFlow1.flowPort_a) annotation(
      Line(points = {{-60, 0}, {-48, 0}, {-48, 0}, {-48, 0}}, color = {255, 0, 0}));
    connect(volumeFlow1.flowPort_b, heatedPipe1.flowPort_a) annotation(
      Line(points = {{-28, 0}, {-10, 0}, {-10, 0}, {-10, 0}}, color = {255, 0, 0}));
    connect(heatedPipe1.flowPort_b, ambient1.flowPort) annotation(
      Line(points = {{10, 0}, {46, 0}, {46, 0}, {46, 0}}, color = {255, 0, 0}));
  end HeatedPipeTester;




  model HeatedPipeTester2
    parameter Modelica.Thermal.FluidHeatFlow.Media.Medium medium = Modelica.Thermal.FluidHeatFlow.Media.Medium() "Cooling medium" annotation(
      choicesAllMatching = true);
    parameter Modelica.SIunits.Temperature TAmb(displayUnit = "degC") = 293.15 "Ambient temperature";
    Modelica.Thermal.FluidHeatFlow.Sources.VolumeFlow volumeFlow1 annotation(
      Placement(visible = true, transformation(origin = {-38, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Components.HeatedPipe heatedPipe1(medium = medium, T0 = TAmb, m = 0.1, V_flowLaminar = 0.1, dpLaminar(displayUnit = "Pa") = 0.1, V_flowNominal = 1, dpNominal(displayUnit = "Pa") = 1, h_g = 0, T0fixed = true) annotation(
      Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient1 annotation(
      Placement(visible = true, transformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
    Modelica.Thermal.FluidHeatFlow.Sources.Ambient ambient2 annotation(
      Placement(visible = true, transformation(origin = {-70, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
  equation
    connect(ambient2.flowPort, volumeFlow1.flowPort_a) annotation(
      Line(points = {{-60, 0}, {-48, 0}, {-48, 0}, {-48, 0}}, color = {255, 0, 0}));
    connect(volumeFlow1.flowPort_b, heatedPipe1.flowPort_a) annotation(
      Line(points = {{-28, 0}, {-10, 0}, {-10, 0}, {-10, 0}}, color = {255, 0, 0}));
    connect(heatedPipe1.flowPort_b, ambient1.flowPort) annotation(
      Line(points = {{10, 0}, {46, 0}, {46, 0}, {46, 0}}, color = {255, 0, 0}));
  end HeatedPipeTester2;
  annotation(
    uses(Modelica(version = "3.2.2")));
end FlowSensor;
