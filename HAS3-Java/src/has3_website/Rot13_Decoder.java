package has3_website;

public class Rot13_Decoder
{

	public static void main(String[] args)
	{
		System.out.println(rot13("YRNEAFCNPRSNFGRE").toLowerCase());
	}

	public static String rot13(String input)
	{
		char[] characters = input.toCharArray();
		char[] newChars = new char[characters.length];
		for (int i = 0; i < characters.length; i++)
		{
			char x = characters[i];
			x += 13;
			if (x > 0x5A)
			{
				x -= 26;
			}
			newChars[i] = x;
		}
		return new String(newChars);
	}

}
