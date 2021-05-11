# S03 Know Issues list #
This document contains know issues for the ITxPT 2.1.1 S03 specifications. It contains items that someone implementing towards the relevant part of the specification could potentially benefit of being aware of. Items that falls outside of this, e.g. requests for an additional feature are not part of this document.

The expectation is that these issues will be addressed in a future revision of the specification. There is no guarantee that that future specification revision will be in line with implementation advice below; implementation advice is a best-effort attempt to outline something that will cause the least amount of problems and/or are most likely to be in line with a future specification update. The implementation advice may change without notice!

# S03 Known Issues #

## S03 P01 TiGR ##

### General – Ignition and other “combustion states” ###
**Issue:** The specification was originally developed for combustion engine vehicles. This means it is not always a good fit for hybrid and – particularly – electric vehicles, because multiple drive units are not supported, and because an EV vehicle does not have the physical states found in a combustion vehicle. 

**Note:** Multiple items/issues relating to this was received late in the 2.1.1 update process. It was decided that it would be better to not try to fix these at the last minute, but rather take the time for a full revision of the spec regarding these aspects. 

**Implementation advice:** For hybrids, drivetrain items that exists once, even if there are two drivetrains, should be for the combustion engine, rather than some combination of the two drivetrains. For conditions, like Ignition, that may not match well to actual signals/states in a hybrid/electrical vehicle these should be considered logical states rather than physical signals. E.g. perhaps there is isn’t a good Ignition signal in a EV. But there _is_ a state where “pressing the accelerator pedal will apply torque to the wheels”, and this could then be considered the “Ignintion==On” in an EV for spec purposes. 
