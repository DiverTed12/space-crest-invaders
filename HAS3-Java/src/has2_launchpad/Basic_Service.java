package has2_launchpad;

import java.net.UnknownHostException;

import utilities.SocketCommunicator;

public class Basic_Service
{
	static String serverAddr = "73.134.113.199";
	static int serverPort = 5000;

	public static void main(String[] args)
	{
		try
		{
			SocketCommunicator comms = new SocketCommunicator(serverAddr, serverPort);

			String line = comms.receive();

			System.out.println(line);
			String[] tokens = line.split(" ");
			int sum = 0;
			for (String s : tokens)
			{
				int number;
				try
				{
					number = Integer.parseInt(s); // If it's an invalid number, exception
					sum += number; // Otherwise, add it to the sum
				} catch (Exception e)
				{
					// Do Nothing with things not numbers
				}

			}
			System.out.println(sum);
			comms.send(String.valueOf(sum));

			String success = comms.receive();
			System.out.println(success);

			comms.close();
		} catch (UnknownHostException e)
		{
			e.printStackTrace();
		} catch (Exception e)
		{
			e.printStackTrace();
		}
	}

}
