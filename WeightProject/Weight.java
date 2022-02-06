public class Weight 
/* Alfred Conrad Santos, CMIS 242/6382, 25 Jan 2022 */
{
	private int pounds;
	private double ounces;
	private final int ouncesInPound = 16;
	
	public Weight(int pounds, double ounces) /*  A public constructor that allows the pounds and ounces to be initialized to the values
	supplied as parameters. */
	{
		this.pounds = pounds;
		this.ounces = ounces;
	}
	
	public boolean lessThan(Weight w) /* A public instance method named lessThan that accepts one weight as a parameter and
returns whether the weight object on which it is invoked is less than the weight supplied
as a parameter. */
	{
		if(this.pounds < w.pounds)
			return true;
		else if(this.pounds == w.pounds && this.ounces < w.ounces)
			return true;
		else
			return false;
	}
	
	public void addTo(Weight w) /* A public instance method named addTo that accepts one weight as a parameter and adds
the weight supplied as a parameter to the weight object on which it is invoked. It should
normalize the result. */
	{
		double w1 = this.toOunces();
		double w2 = w.toOunces();
		
		this.ounces = w1 + w2;

		this.normalize();
	}
	
	public String toString() /* A public instance toString method that returns a string that looks as follows: x lbs y oz,
	where x is the number of pounds and y the number of ounces. The number of ounces
	should be displayed with two places to the right of the decimal. You will use this method
	to print out the weight for display purposes. */
	{
		String data = this.pounds + " lbs " + String.format("%.2f oz", this.ounces);
		return data;
	}
	
	private double toOunces() /* A private instance method toOunces that returns the total number of ounces in the weight
object on which it was invoked. This private method will be used (re-used) within the
Weight class to help with various computations */
	{
		double oun = (this.pounds * ouncesInPound) + this.ounces;
		return oun;		
	}
	
	private void normalize() /* A private instance method normalize that normalizes the weight on which it was
invoked by ensuring that the number of ounces is less than the number of ounces in a
pound. This private method will be used (re-used) within the Weight class to help with
various computations */
	{		
		int pound = ((int) this.ounces) / ouncesInPound;
		
		this.pounds = pound;
		
		this.ounces = this.ounces - (pound * ouncesInPound);
	}
}