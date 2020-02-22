package fr.charleslabs.beamforming;

/**
 * This Java class generates Arduino Uno/Nano code
 * to create N phased square waves for N
 * channel audio beamforming.
 * <br>
 * Note : Requires the "A328_PINS.h" header file
 * for fast, consistent pin commutation timing.
 * <br>
 * Note 2 : To plot the result in a spreadsheet, 
 * use the arduino_sg.awk AWK script.
 * 
 * @author CGrassin
 *
 */
public class BeamformingCodeGenerator {
	
	/**
	 * Hard-coded code generation, change parameters accordingly.
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		String[] pins = new String[]{"D2","D3","D4","D5","D6","D7"/*,"D8","D9","D10","D11","D12","D13"*/};
		
		// Includes/Defines
		System.out.println("#include \"A328_PINS.h\"\n");
		
		// Setup
		System.out.println("void setup(){");
		for(String pin : pins)
			System.out.println("_PIN_CONFIG_OUT( _" + pin + " );");
		System.out.println("}\n");
		
		// Loop
		System.out.println("void loop(){");
		System.out.print(generate_code(pins,340/*m/s*/,0.15/*m*/,0*2d*Math.PI/360d/*rad*/,1000/*Hz*/));
		System.out.println("}");
	}
	
	//----------------------------
	
	/**
	 * Internal class to group information on
	 * a channel.
	 */
	private static class Channel{
		public boolean status = false;
		public double deadline = 0;
		public String pinName;
		
		public Channel(boolean initStatus, double deadline, String pinName){
			this.deadline = deadline;
			this.status = initStatus;
			this.pinName = pinName;
		}
		
		public String togglePin(double nextDeadline) {
			this.status = !this.status;
			this.deadline = nextDeadline;
			return ("_PIN_WRITE( _" + this.pinName + " , " + (this.status?1:0) + " );\n");
		}
	}
	
	/**
	 * Generates the signal generation code.
	 * 
	 * @param pins Array containing the position of the N pins. Warning: position is critical.
	 * @param c Velocity of the wave (air at 20�C = 343 m/s).
	 * @param d Spacing between the speakers (m).
	 * @param theta Offset angle (rad).
	 * @param f Frequency of the signal (Hz).
	 * @return The C code to loop for signal generation.
	 */
	public static String generate_code(final String[] pins, final double c, final double d, final double theta, final double f) throws Exception{
		StringBuilder code = new StringBuilder();
		
		final double duty_cycle = 0.5; // >0 && <1
		
		// Compute physics constants
		final double lambda = c / f; //m
		final double period = 1d / f * 1e6; // us
		final double phi = 2d * Math.PI * d * Math.sin(theta) / lambda; //rad
		final double phi_delta_t = phi / (2d * Math.PI * f) * 1e6; // us
		
		// Print input parameters
		code.append("/* Beamforming Code Parameters :\n");
		code.append("* theta = "+theta+" rad \n");
		code.append("* c = "+c+" m/s\n");
		code.append("* d = "+d+" m\n");
		code.append("* f = "+f+" Hz\n");
		code.append("* far_field_d = "+2d*Math.pow(d*pins.length, 2)/lambda+" m */\n"); // Fraunhofer distance
		
		// Sanity checks on parameters
		if(pins.length < 1)
			throw new Exception("Array should contain at least one pin.");
		if(c<=0 || d<=0 || f<=0)
			throw new Exception("c, d and f must be > 0.");
		if(d > lambda / (1 + Math.abs(Math.sin(theta))))
			code.append("/* WARNING: grating lobes detected (reduce theta or f)! */\n");
		if(phi_delta_t > 0 && phi_delta_t < 5)
			code.append("/* WARNING: time between pin toggles is very short (increase theta or reduce f)! */\n");
		
		// Prepare pins array with t=0 states
		Channel[] channels = new Channel[pins.length];
		for(int i=0; i< channels.length;i++){
			final double delta_t = ((i * phi_delta_t) % period + period) % period;
			// Two cases: either initially high or initially low
			if(delta_t - duty_cycle * period > 0)
				channels[i] = new Channel(true, delta_t - duty_cycle * period, pins[i]); 
			else
				channels[i] = new Channel(false, delta_t , pins[i]); 
		}
					
		// Code generation (from t=0 to t=period)
		double delay, currenttime=0;
		while(currenttime < period) {
			
			// Pin status and next deadline
			delay = channels[0].deadline;
			for(int i=0; i< channels.length;i++) {
				// If some deadline is reached
				if (channels[i].deadline <= 0)
					code.append(channels[i].togglePin(duty_cycle*period));
				
				// Look for next smallest deadline
				delay = Math.min(delay, channels[i].deadline);
			}
			
			// Apply delay
			currenttime+=delay;
			if(Math.round(delay) > 0) 
				code.append("delayMicroseconds( "+Math.round(delay)+ " );\n");
			for(int i=0; i< channels.length;i++)
				channels[i].deadline -= delay;
		}
		
		return code.toString();
	}
}
