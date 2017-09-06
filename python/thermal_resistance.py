from heat_pipe_data import *

# A precise model is needed for
# external evaporator resistance;
# It will depend on our system,
# how it is build.
R_ext_e = 0

# A precise model is needed for
# external condenser resistance;
# It will depend on our system,
# how it is build.
R_ext_c = 0

Rpe = numpy.log(pipe_external_diameter/pipe_internal_diameter) / (2*numpy.pi*length_evaporator*pipe_thermal_conduction)
Rpc = numpy.log(pipe_external_diameter/pipe_internal_diameter) / (2*numpy.pi*length_condenser*pipe_thermal_conduction)
Rwe = numpy.log(pipe_internal_diameter/diameter_steam) / (2*numpy.pi*length_evaporator*mesh_effective_conduction)
Rwc = numpy.log(pipe_external_diameter/pipe_internal_diameter) / (2*numpy.pi*length_condenser*pipe_thermal_conduction)

Rp = Rpe/2 + Rpa + Rpc/2
Rw = Rpe + Rwe/2 + Rwa + Rwc/2 + Rpc
Rv = Rpe + Rwe + Rie + Rva + Ric + Rwc + Rpc
Rt = R_ext_e + (1/Rp + 1/Rw + 1/Rv)**(-1) + R_ext_c
