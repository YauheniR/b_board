import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { BbService } from "./bb.service";


@Component({
  selector: 'app-bb-detail',
  templateUrl: './bb-detail.component.html',
  styleUrls: ['./bb-detail.component.css']
})
export class BbDetailComponent implements OnInit {
  bb: any;
  comments: any;
  author: String = '';
  password: String = '';
  content: String = '';

  constructor(private bbservice: BbService, private ar: ActivatedRoute) { }

  getComments() {
    this.bbservice.getComment(this.bb.id).subscribe((comments: Object[]) => {this.comments = comments;})
  }

  submitComment() {
    this.bbservice.addComment(this.bb.id, this.author, this.password, this.content).subscribe((comment: Object) => {
      if (comment) {
        this.content = "";
        this.getComments();
      }
    })
  }

  ngOnInit(): void {
    const pk = this.ar.snapshot.params.pk;
    this.bbservice.getBb(pk).subscribe((bb: Object) => {this.bb = bb; this.getComments();})
  }

}
