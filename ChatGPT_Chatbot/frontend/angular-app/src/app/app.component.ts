import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit, OnDestroy {
  inputValue: string = '';
  receivedMessage: string = '';
  socket: WebSocket | null = null;

  ngOnInit() {
    this.socket = new WebSocket('ws://localhost:8000/chat');

    this.socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    this.socket.onmessage = (event) => {
      this.receivedMessage = event.data;
      console.log(this.receivedMessage);
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  }

  ngOnDestroy() {
    if (this.socket) {
      this.socket.close();
    }
  }

  sendMessage(event: MouseEvent) {
    event.preventDefault();
    if (this.inputValue) {
      // if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      //   this.socket = new WebSocket('ws://localhost:8000/chat');

      //   this.socket.onopen = () => {
      //     console.log('WebSocket connection established');
      //     this.socket.send(this.inputValue);
      //     console.log(this.inputValue)
      //   };

      //   this.socket.onmessage = (event) => {
      //     this.receivedMessage = event.data;
      //     console.log(this.receivedMessage);
      //     this.socket.close();
      //   };

      //   this.socket.onclose = () => {
      //     console.log('WebSocket connection closed');
      //   };
      // }
      // else {
      //   this.socket.send(this.inputValue);
      //   console.log(this.inputValue)
      // }
      this.socket.send(this.inputValue);
      console.log(this.inputValue)
      this.inputValue = '';
    }
  }


}