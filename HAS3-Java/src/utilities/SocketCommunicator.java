package utilities;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.net.Socket;

/**
 * The SocketCommunicator Utility can be used to communicate with the
 * challenges. It encapsulates the sending and receiving on a socket. An example
 * of this being used can be seen in the Basic_Service class.
 * 
 * @author Joe
 *
 */
public class SocketCommunicator
{
	public static int READ_BYTE_LENGTH = 1024; // This might need to be changed for larger strings.

	String serverAddr;
	int serverPort;
	Socket clientSocket;
	BufferedInputStream bis;
	BufferedOutputStream bos;

	public SocketCommunicator(String serverAddr, int serverPort) throws Exception
	{
		this.serverAddr = serverAddr;
		this.serverPort = serverPort;
		System.err.print("Connecting to " + serverAddr + ":" + serverPort + "...");
		clientSocket = new Socket(serverAddr, serverPort);
		bis = new BufferedInputStream(clientSocket.getInputStream());
		bos = new BufferedOutputStream(clientSocket.getOutputStream());
		System.err.println("Connected!");
	}

	public String receive() throws Exception
	{
		byte[] bytesRead = new byte[READ_BYTE_LENGTH];
		bis.read(bytesRead);
		String readStr = new String(bytesRead);
		System.err.println(readStr);
		return readStr;
	}

	public void send(String sendStr) throws Exception
	{
		String outputStr = sendStr + "\n\r";
		bos.write(outputStr.getBytes());
		bos.flush();
	}

	public void close() throws Exception
	{
		clientSocket.close();
	}

}
